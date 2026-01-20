from celery import shared_task
import os
import csv
from datetime import datetime
from Backend.models import Professional, User, Booking,Service,Customer
from flask import current_app,render_template
# import flask_excel as excel
from Backend.celery.mail import send_mail
from datetime import datetime, timedelta


@shared_task(bind=True, ignore_result=False)
def export_closed_service_requests_csv(self):
    import flask_excel as excel 
    print(" Starting CSV generation for closed service requests...")

 
    closed_bookings = Booking.query.filter(Booking.status == 'Completed').all()


    header = ['Booking ID', 'Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Service Date', 'Remarks']
    csv_data = []

    for booking in closed_bookings:
        remarks = ", ".join([r.feedback for r in booking.review]) if booking.review else "No Remarks"

        csv_data.append([
            booking.id,
            booking.service_id if booking.service else "N/A",
            booking.customer_id if booking.customer else "N/A",
            booking.professional_id if booking.professional else "N/A",
            booking.date.strftime('%Y-%m-%d'),
            booking.service_date.strftime('%Y-%m-%d'),
            remarks
        ])

 
    folder_path = os.path.join(os.getcwd(), 'user-downloads')
    os.makedirs(folder_path, exist_ok=True)

    # ✅ Create CSV file with only date in filename
    csv_file_path = os.path.join(folder_path, 'closed_service_requests.csv')

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header row
        writer.writerows(csv_data)  # Write data rows

    print(f"✅ CSV saved at: {csv_file_path}")
    return csv_file_path


@shared_task(ignore_result=True)
def pending_bookings_reminder():
    print(" Checking for pending bookings...")

    # Get all pending bookings with no professional assigned
    pending_bookings = Booking.query.filter_by(
        status='Pending',
        professional_id=None
    ).all()

    print(f" Found {len(pending_bookings)} pending bookings.")

    for booking in pending_bookings:
        service = booking.service
        customer = booking.customer
        customer_user = customer.user if customer else None

        if not service or not customer_user:
            continue

        # Find professionals who provide this service
        professionals = Professional.query.filter_by(service_id=service.id).all()

        for professional in professionals:
            user = professional.user

            # Skip blocked users
            if not user or user.is_blocked:
                continue

            print(f" Sending email to professional: {user.email}")

            content = render_template(
                "pending_booking_reminder.html",
                username=user.username,                        
                service_name=service.name,
                customer_name=customer_user.username,            
                requested_date=booking.service_date.strftime("%Y-%m-%d")  
            )

            subject = "New Service Request Available"

            send_mail(user.email, subject, content)

    print(" Pending booking reminder emails sent.")



@shared_task(ignore_result=True)
def send_monthly_activity_report():
    
    print(" Generating monthly activity reports for customers...")

    # Get the first date of the current month
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)

    # Fetch all customers
    customers = Customer.query.all()
    
    for customer in customers:
        # Get completed bookings after the 1st of the current month
        completed_bookings = Booking.query.filter(
            Booking.customer_id == customer.id,
            Booking.service_date >= first_day_of_current_month,
            Booking.status.ilike('Completed') 
        ).all()

        # Get canceled bookings after the 1st of the current month
        canceled_bookings = Booking.query.filter(
            Booking.customer_id == customer.id,
            Booking.service_date >= first_day_of_current_month,
            Booking.status.ilike('Cancelled')  # Case-insensitive match
        ).all()

        # Count the bookings
        completed_services = len(completed_bookings)
        canceled_services = len(canceled_bookings)
        service_details = []

        # Loop through bookings to collect service details
        for booking in completed_bookings + canceled_bookings:
            service = Service.query.get(booking.service_id)
            if service:
                service_details.append({
                    'service_name': service.name,
                    'status': booking.status,
                    'service_date': booking.service_date.strftime("%Y-%m-%d")
                })

        # Prepare the report data
        report_data = {
            'service_details': service_details,
            'completed_services': completed_services,
            'canceled_services': canceled_services,
            'month': first_day_of_current_month.strftime("%B %Y"),
            'username': customer.user.username
        }

        # Send the email to the customer
        subject = f"Your Monthly Activity Report - {report_data['month']}"
        content = render_template('monthly_report.html', **report_data)

        # Ensure the user is not blocked before sending the email
        if customer.user and not customer.user.is_blocked:
            print(f"🔹 Sending monthly report to: {customer.user.email}")
            send_mail(customer.user.email, subject, content)

    print(" Monthly activity reports sent to all customers.")


@shared_task(ignore_result=True)
def send_customer_booking_confirmation(booking_id):
    print(f" Sending booking confirmation for booking ID: {booking_id}")

    booking = Booking.query.get(booking_id)

    if not booking:
        print(" Booking not found.")
        return

    customer = booking.customer
    user = customer.user if customer else None
    service = booking.service

     # Safety checks
    if not user or user.is_blocked:
        print(" Customer not found or user is blocked.")
        return

    # Prepare email data
    email_data = {
        "username": user.username,
        "service_name": service.name if service else "Service",
        "service_date": booking.service_date.strftime("%Y-%m-%d"),
        "booking_id": booking.id,
        "status": booking.status,
        "booking_date": booking.date.strftime("%Y-%m-%d"),
    }

    subject = "Booking Confirmed – Fixify"

    # Render HTML email template
    content = render_template(
        "customer_booking_confirmation.html",
        **email_data
    )

    # Send email
    send_mail(user.email, subject, content)

    print(f" Booking confirmation email sent to {user.email}")




@shared_task(ignore_result=True)
def send_service_completion_email(booking_id):
    print(f" Sending service completion email for booking ID: {booking_id}")

    booking = Booking.query.get(booking_id)

    if not booking:
        print(" Booking not found.")
        return

    customer = booking.customer
    user = customer.user if customer else None
    service = booking.service
    professional = booking.professional
    professional_user = professional.user if professional else None

    if not user or user.is_blocked:
        print(" Customer invalid or blocked.")
        return

    content = render_template(
        "customer_service_completion.html",
        username=user.username,
        service_name=service.name if service else "Service",
        service_date=booking.service_date.strftime("%Y-%m-%d"),
        professional_name=professional_user.username if professional_user else "Professional",
        booking_id=booking.id
    )

    subject = "Service Completed Successfully – Fixify"

    send_mail(user.email, subject, content)

    print(f" Service completion email sent to {user.email}")
