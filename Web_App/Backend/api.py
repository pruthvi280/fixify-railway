from flask_restful import Api, reqparse, fields, marshal_with, abort, Resource
from flask import Blueprint, request, jsonify,send_file,url_for
from .authorization import SignUp, Login, Logout,Ping
from .models import User,Category, Service, db,Professional,Booking,Customer,Review,Payment,Professional_rejected_bookings
import os
from flask_jwt_extended import get_jwt_identity,jwt_required
from datetime import datetime 
from sqlalchemy.sql import func
from .cache import cache
import time
from Backend.celery.tasks import export_closed_service_requests_csv,send_customer_booking_confirmation,send_service_completion_email
from celery.result import AsyncResult 
from collections import Counter
from flask import send_from_directory


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Ping, "/ping")



category_fields = {
  "id": fields.Integer,
  "name": fields.String,
  "services": fields.List(fields.String)
}

# Service Fields
service_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'description': fields.String,
  'base_price': fields.Float,
  'category': fields.String
}

class MyCategory(Resource):
  def post(self):
    data = request.get_json()
    category_name = data.get("name")
    
    if Category.query.filter_by(name=category_name).first():
      abort(409, message="Category already exists.")

    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()

    return {"message": "Category created", "id": category.id}, 201

  def get(self):
    categories = Category.query.all()
    return jsonify([{'id': category.id, 'name': category.name} for category in categories])

  def delete(self, category_id):
    category = Category.query.get_or_404(category_id)
      
    # Ensure the category has no services before deletion
    if Service.query.filter_by(category_id=category.id).first():
      abort(400, message="Cannot delete category with associated services.")
    
    db.session.delete(category)
    db.session.commit()
    return {"message": "Category deleted"}

class MyService(Resource):
  def post(self):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    base_price = data.get('base_price')
    category_id = data.get('category')
    category = Category.query.get(category_id)

    if not category:
        abort(404, message="Category not found")

    existing_service = Service.query.filter_by(name=name, category_id=category.id).first()
    if existing_service:
        abort(409, message="Service with the same name already exists under this category.")

    service = Service(
        name=name,
        description=description,
        base_price=base_price,
        category_id=category.id,
    )
    db.session.add(service)
    db.session.commit()

    return {"message": "Service created", "id": service.id}, 201

  def get(self, service_id=None):
        if service_id:
            service = Service.query.get_or_404(service_id)
            return jsonify({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'base_price': service.base_price,
                'category': service.category.name,
                'category_id': service.category_id
            })
        else:
            services = Service.query.all()
            return jsonify([
                {
                    'id': service.id,
                    'name': service.name,
                    'description': service.description,
                    'base_price': service.base_price,
                    'category': service.category.name,
                    'category_id': service.category_id
                } 
                for service in services
            ])

  def put(self, service_id):
    data = request.get_json()
    service = Service.query.get_or_404(service_id)

    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    base_price = data.get('base_price')

    if not name or not description or base_price is None:
        abort(400, message="Name, description, and base price are required fields.")

 
    if 'category' in data:
      category = Category.query.get(data['category']) 
      if category:
          service.category_id = category.id
      else:
          abort(404, message="Category not found")
    

    existing_service = Service.query.filter_by(name=name, category_id=service.category_id).first()
    if existing_service and existing_service.id != service.id:
        abort(409, message="Service with the same name already exists under this category.")
      
    service.name = name
    service.description = description
    service.base_price = base_price

    db.session.commit()
    return {"message": "Service updated", "id": service.id}

  def delete(self, service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return {"message": "Service deleted"}

api.add_resource(MyCategory, '/categories', '/categories/<int:category_id>')
api.add_resource(MyService, '/services', '/services/<int:service_id>')


class ManageProfessionals(Resource):
    
    def get(self):
      professionals = User.query.filter_by(role="professional").all()

      return jsonify([
          {
            "id": professional.id,
            "name": professional.username,
            "service": professional.Professional_dets.service.name if professional.Professional_dets and professional.Professional_dets.service else "N/A",
            "resume": f"/uploads/{os.path.basename(professional.Professional_dets.document)}"
            if professional.Professional_dets and professional.Professional_dets.document else None,
            "status": "Approved" if professional.approved else "Blocked" if professional.is_blocked else "Pending",
          }
          for professional in professionals
      ])

    def put(self, professional_id):
        # Get the data from the request
        data = request.get_json()
        new_status = data.get("status")

        # Validate the status
        if new_status not in ["Approved", "Rejected", "Blocked"]:
            abort(400, message="Invalid status")

        # Fetch the User object for the professional
        user = User.query.get_or_404(professional_id)

        # Update status based on new status
        if new_status == "Approved":
            user.approved = True
            user.is_blocked = False  
        elif new_status == "Blocked":
            user.approved = False  
            user.is_blocked = True  # Mark as blocked
        elif new_status == "Rejected":
            user.approved = False
            user.is_blocked = False  

        db.session.commit()
        return {"message": f"Professional status updated to {new_status}"}, 200

    def delete(self, professional_id):
      user = User.query.get_or_404(professional_id)

      db.session.delete(user)
      db.session.commit()

      return {"message": "Professional deleted successfully."}, 200

api.add_resource(ManageProfessionals, '/professionals', '/professionals/<int:professional_id>')



class ManageCustomers(Resource):
  def get(self):
    customers=Customer.query.all()
    customer_list=[{
        "id": customer.id,
        "user_id": customer.user.id,
        "username": customer.user.username,
        "email": customer.user.email,
        "phone_no": customer.phone_no,
        "address": customer.address,
        "is_blocked": customer.user.is_blocked
    } for customer in customers]

    return jsonify(customer_list)
   
  def put(self,user_id):
    user=User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404
    
    user.is_blocked = not user.is_blocked  
    db.session.commit()
    status = "blocked" if user.is_blocked else "unblocked"
    return {"message": f"User {status} successfully"}, 200
  
  def delete(self, user_id):
      user = User.query.get(user_id)
      if not user:
         return {"message": "User not found"}, 404

      if not user.is_blocked:
         return {"message": "User must be blocked before deletion"}, 400

      db.session.delete(user)
      db.session.commit()
      return {"message": "User deleted successfully"}, 200
   

api.add_resource(ManageCustomers, "/managecustomers", "/managecustomers/<int:user_id>")


class GetServices(Resource):
  def get(self, category_id=None):
   
    if category_id:
        category = Category.query.get_or_404(category_id)
        services = Service.query.filter_by(category_id=category.id).all()
    else:
        # If no category_id is provided, fetch all services across categories
        services = Service.query.all()

    # Return services with relevant information
    return jsonify([
        {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'base_price': service.base_price,
            'category': service.category.name
        }
        for service in services
    ])

api.add_resource(GetServices, '/getservices', '/getservices/<int:category_id>')


class AllBookingsOverview(Resource):
  @jwt_required()
  def get(self):
    user_identity=get_jwt_identity()
    user_id=user_identity["id"]
    user_role=user_identity["role"]

    if user_role!="admin":
      return {"message": "Unauthorized access"}, 403
    
    bookings=Booking.query.all()
    booking_list=[]
    print(len(bookings))
    for booking in bookings:
      
      customer_name= booking.customer.user.username if booking.customer else "N/A"

      professional_name=booking.professional.user.username if booking.professional else "N/A"

      service_name = booking.service.name if booking.service else "N/A"
      booking_list.append({
        "id": booking.id,
        "customer_name": customer_name,
        "service_name": service_name,
        "professional_name": professional_name,
        "booking_date": booking.date.strftime("%Y-%m-%d"),
        "status": booking.status
      })

    return {"bookings":booking_list},200

api.add_resource(AllBookingsOverview, '/bookingsoverview')


class AdminStats(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()["id"]

    user=User.query.get(user_id)
    if user.role!="admin":
      return {"message":"Access denaied: Admins Only"},403
    
    try:
      total_customers=Customer.query.count()
      total_services = Service.query.count()
      new_bookings = Booking.query.filter(Booking.status == 'Pending').count()

      return {
        "total_customers": total_customers,
        "total_services": total_services,
        "new_bookings": new_bookings,
      },200
    
    except Exception as e:
      return {"message": f"An error occurred: {str(e)}"}, 500
    
api.add_resource(AdminStats,'/adminstats')


class MostPopularService(Resource):
    def get(self):
      # Fetch all bookings
      all_bookings = Booking.query.with_entities(Booking.service_id).all()

      # Count occurrences of each service_id
      service_counts = Counter([booking.service_id for booking in all_bookings if booking.service_id])

      if not service_counts:
          return jsonify({"message": "No bookings found", "most_popular_services": []})

      # Find the highest booking count
      max_count = max(service_counts.values())

      # Get all services with this max_count (handles ties)
      most_popular_service_ids = [service_id for service_id, count in service_counts.items() if count == max_count]

      # Fetch service details
      most_popular_services = Service.query.filter(Service.id.in_(most_popular_service_ids)).all()

      return jsonify({
          "most_popular_services": [
              {
                  "id": service.id,
                  "name": service.name,
                  "description": service.description,
                  "base_price": service.base_price
              }
              for service in most_popular_services
          ]
      })

api.add_resource(MostPopularService, "/most_popular_service")


##########################################above api is for admin######################

class RequestService(Resource):
  @jwt_required()
  def post(self):
    try:
      # Get request data
      data = request.get_json()
      service_id = data.get("service_id")
      service_date = data.get("service_date")

      # Validate required fields
      if not service_id:
          return {"message": "Service ID is required."}, 400
      if not service_date:
          return {"message": "Service date is required."}, 400

      # Check if service exists
      service = Service.query.get(service_id)
      if not service:
          return {"message": "Service not found."}, 404

      # --- FIX START: Handle Identity Safely ---
      raw_identity = get_jwt_identity()
      
      # The identity might be a simple string ID "1" or a dictionary
      if isinstance(raw_identity, dict):
          user_id = raw_identity.get("id")
      elif isinstance(raw_identity, str):
          # If it's a string, try to parse it as a dict, otherwise assume it IS the ID
          import ast
          try:
              user_data = ast.literal_eval(raw_identity)
              if isinstance(user_data, dict):
                  user_id = user_data.get("id")
              else:
                  user_id = raw_identity
          except:
              user_id = raw_identity
      else:
          user_id = raw_identity
      # --- FIX END ---

      # Get customer details
      customer = Customer.query.filter_by(user_id=user_id).first()
      if not customer:
          return {"message": "Customer not found."}, 404

      # Create a new booking
      from datetime import datetime
      new_booking = Booking(
          service_id=service.id,
          customer_id=customer.id,
          professional_id=None,
          service_date=datetime.strptime(service_date, "%Y-%m-%d"),
          date=datetime.now()
      )

      # Save booking to the database
      db.session.add(new_booking)
      db.session.commit()

      # Send confirmation (inside try/except to prevent crash if Redis/Email fails)
      try:
          # send_customer_booking_confirmation.delay(new_booking.id)
          cache.delete(f"mybookings_{customer.user_id}")
      except:
          pass

      return {"message": "Service requested successfully!", "booking_id": new_booking.id}, 201

    except Exception as e:
      print(f"ERROR in RequestService: {str(e)}") # Log error to console
      return {"message": f"An error occurred: {str(e)}"}, 500

class OngoingServices(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()["id"]
    customer = Customer.query.filter_by(user_id = user_id).first_or_404()
    customer_id = customer.id
    ongoing_bookings = Booking.query.filter(
      Booking.customer_id == customer_id, 
      Booking.status.in_(["Pending", "Accepted"])
    ).all()

    result = []
    for booking in ongoing_bookings:
      service = Service.query.get(booking.service_id)
      professional_name = "Not Assigned"
      professional_contact = "Not Assigned"
      professional_rating = 0
      amount=service.base_price if service else 0

      if booking.professional_id:
        professional = Professional.query.get(booking.professional_id)
        user = User.query.get(professional.user_id) if professional else None

        if user:
          professional_name = user.username
          professional_contact = professional.phone_no

        avg_rating = db.session.query(func.avg(Review.rating)).join(Booking).filter(
              Booking.professional_id == professional.id
          ).scalar()
        professional_rating = round(avg_rating, 1) if avg_rating else 0

      # ✅ Fix: Convert date to a string to avoid JSON serialization issues
      booking_date = booking.date.strftime("%Y-%m-%d") if isinstance(booking.date, datetime) else booking.date

      result.append({
        "id": booking.id,
        "service_name": service.name if service else "Unknown Service",
        "professional_name": professional_name,
        "professional_contact": professional_contact,
        "date": booking_date,
        "scheduledDate": booking.service_date.strftime("%Y-%m-%d"),
        "status": booking.status,
        "professional_rating": professional_rating,
        "amount":amount
      })
    return result, 200 
  
  @jwt_required()
  def put(self):
    data=request.json
    booking_id = data.get("booking_id")
    new_scheduled_date = data.get("scheduled_date")
 

    if not booking_id:
      return {"message": "Booking ID is required"}, 400
    
    booking = Booking.query.get(booking_id)
    if not booking:
      return {"message": "Booking not found"}, 404
    
    if booking.status != "Pending":
      return {"message": "Only pending bookings can be rescheduled"}, 400
    
    booking.service_date = datetime.strptime(new_scheduled_date, "%Y-%m-%d")
    db.session.commit()
    return {"message": "Booking rescheduled successfully"}, 200

api.add_resource(OngoingServices, "/ongoingservices")


class CancelBooking(Resource):
  @jwt_required()
  def post(self, booking_id):
    booking = Booking.query.get(booking_id)
    
    if not booking:
      return {"message": "Booking not found"}, 404
    
    if booking.professional_id:
      return {"message": "Cannot cancel booking after a professional is assigned"}, 400
    
    booking.status = "Cancelled"
    db.session.commit()

    #  Update cache instead of deleting it
    cache_key = f"mybookings_{booking.customer.user_id}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        for item in cached_data:
            if item["id"] == booking.id:
                item["status"] = "Pending"  
        

        cache.set(cache_key, cached_data, timeout=20)

    return {"message": "Booking cancelled successfully"}, 200

api.add_resource(CancelBooking, "/cancelbooking/<int:booking_id>")


class UpdateScheduledDate(Resource):
   @jwt_required()
   def put(self,booking_id):
      user_identity = get_jwt_identity()
      print(f"Full JWT Identity: {user_identity}")

      # Extract user ID safely
      user_id = user_identity.get("id") if isinstance(user_identity, dict) else user_identity

      data=request.json
      new_service_date=data.get("scheduled_date")

      if not new_service_date:
        return {'message': 'Service date is required.'}, 400
      
      try:
        new_service_date = datetime.strptime(new_service_date, '%Y-%m-%d')
      except:
        return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400
      
      booking = Booking.query.filter_by(id=booking_id).first()
      print(f"Found Booking: {booking}") 
      if not booking:
        return {'message': 'Booking not found or not authorized.'}, 404
      
      
      booking.service_date=new_service_date
      db.session.commit()


      return {'message': 'Scheduled date updated successfully.'}, 200

   
api.add_resource(UpdateScheduledDate, '/bookings/<int:booking_id>/update-date')


class BookingStats(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()["id"]
    customer = Customer.query.filter_by(user_id = user_id).first_or_404()
    customer_id = customer.id
    customer_name = customer.user.username
 
    total_bookings=Booking.query.filter_by(customer_id=customer_id).count()
    pending_services=Booking.query.filter_by(customer_id=customer_id,status="Pending").count()
    ongoing_services=Booking.query.filter(Booking.customer_id==customer_id,Booking.status.in_(["Accepted", "Pending"])).count()
    completed_services=Booking.query.filter_by(customer_id=customer_id,status="Completed").count()

    return {
      "total_bookings": total_bookings,
      "pending_services": pending_services,
      "ongoing_services": ongoing_services,
      "completed_services": completed_services,
      "name":customer_name
    }, 200

api.add_resource(BookingStats, '/bookingstats')


class MyBookings(Resource):
  @jwt_required()
  def get(self):
    user_data=get_jwt_identity()
    user_id=user_data.get("id")

    if not user_id:
      return {"error"" Invalid token"},401
    
    customer=Customer.query.filter_by(user_id=user_id).first()
    if not customer:
      return {"error": "Customer not found"}, 404
    
    cache_key = f"mybookings_{user_id}"
    
    #  Check cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data)
    

    bookings = Booking.query.filter_by(customer_id=customer.id).all()

    booking_list=[{
      "id": booking.id,
      "service_name": booking.service.name if booking.service else "Service Not Found",
      "professional_name": booking.professional.user.username if booking.professional else "Not Assigned",
      "date": booking.date.strftime("%Y-%m-%d %H:%M:%S"),
      "service_date": booking.service_date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(booking.service_date, datetime) else "Not Scheduled",
      "status": booking.status,
    } for booking in bookings]

    cache.set(cache_key, booking_list, timeout=20)


    return jsonify(booking_list)
  
api.add_resource(MyBookings, '/mybookings')


class CompletedBookings(Resource):
  @jwt_required()
  def get(self):
    user_identity = get_jwt_identity()
    user_id = user_identity["id"] 

    customer = Customer.query.filter_by(user_id=user_id).first()
    if not customer:
      return {"error": "Customer not found"}, 404
    
    completed_bookings = Booking.query.filter_by(customer_id=customer.id, status="Completed").all()

    completed_services = []
    for booking in completed_bookings:
      professional = booking.professional  # This could be None if the professional was deleted
      review = Review.query.filter_by(booking_id=booking.id).order_by(Review.id.desc()).first()

      completed_services.append({
        "id": booking.id,
        "service_name": booking.service.name if booking.service else "Not Available",
        "professional_name": professional.user.username if professional and professional.user else "Not Available",
        "professional_contact": professional.phone_no if professional else "Not Available",
        "scheduled_date": booking.service_date.strftime("%Y-%m-%d") if booking.service_date else "N/A",
        "rating": review.rating if review else None,
        "feedback": review.feedback if review else None,
      })

    return jsonify(completed_services)

api.add_resource(CompletedBookings, "/completedbookings")



class FeedbackReview(Resource):
  @jwt_required()
  def post(self, booking_id):
    data=request.get_json()

    if not data or "rating" not in data or "feedback" not in data:
      return {"error": "Rating and feedback are required"}, 400
    

    user_identity = get_jwt_identity()
    user_id = user_identity["id"] 

    customer=Customer.query.filter_by(user_id=user_id).first()
    if not customer:
      return {"error": "Only customers can submit reviews"}, 403
    
    booking = Booking.query.filter_by(id=booking_id, customer_id=customer.id).first()
    if not booking:
      return {"error": "Booking not found or unauthorized"}, 404

    
    existing_review = Review.query.filter_by(booking_id=booking_id).first()
    if existing_review:
      return {"error": "You have already submitted a review for this booking"}, 400
    
    new_review = Review(
            booking_id=booking_id,
            rating=data["rating"],
            feedback=data["feedback"]
    )
    db.session.add(new_review)

    booking.status = "Completed"
    db.session.commit()

    send_service_completion_email.delay(booking.id)


    return {"message": "Review submitted successfully and booking marked as completed"}, 201
  
api.add_resource(FeedbackReview, "/feedback/<int:booking_id>")


class MyPayment(Resource):
  @jwt_required()
  def post(self):
    data = request.get_json()
    user_id=get_jwt_identity()

    booking = Booking.query.get(data.get('booking_id'))
    if not booking:
      return {'message': 'Booking not found'}, 404
    
    payment = Payment(
            booking_id=booking.id,
            amount=data.get('amount'),
            method=data.get('method'),
            status='Completed',
            transaction_date=datetime.now()
    )
    db.session.add(payment)
    db.session.commit()

    return {'message': 'Payment successful', 'payment_id': payment.id}, 201


  @jwt_required()
  def get(self,payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
      return {'message': 'Payment not found'}, 404
    
    return {
            'id': payment.id,
            'booking_id': payment.booking_id,
            'amount': payment.amount,
            'method': payment.method,
            'status': payment.status,
            'transaction_date': payment.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
    }, 200
api.add_resource(MyPayment, '/payments', '/payments/<int:payment_id>')
   
#####################above api is for customer#############################

class ProfessionalBookings(Resource):
  @jwt_required()
  def get(self):
    user_identity = get_jwt_identity()
    user_id = user_identity["id"] 

    professional = Professional.query.filter_by(user_id=user_id).first()
    if not professional:
      return {"message": "Professional not found"}, 404
    
    rejected_booking_ids=[ rb.booking_id for rb in Professional_rejected_bookings.query.filter_by(professional_id=professional.id).all()]

    #Fetch pending bookings that have NOT been rejected by this professional
    bookings = Booking.query.filter((Booking.service_id == professional.service_id) & (Booking.status=="Pending") & (~Booking.id.in_(rejected_booking_ids))).all()  # Exclude rejected bookings


    service_requests = [
      {
        "id": booking.id,
        "customerName": booking.customer.user.username,
        "address": booking.customer.address,
        "phone": booking.customer.phone_no,
        "scheduledDate": booking.service_date.strftime("%Y-%m-%d"),
        "serviceName": booking.service.name,
        "status": booking.status,
      }
      for booking in bookings
    ]
    return jsonify(service_requests)
   
  @jwt_required()
  def put(self,booking_id):
    data=request.get_json()
    booking_status=data.get("status")

    if booking_status not in ["Accepted", "Rejected"]:
      return {"message": "Invalid status"}, 400
    
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    current_user = User.query.get(user_id)
    professional=current_user.Professional_dets

    if not professional:
      return {"message": "Professional not found"}, 404
    
    booking=Booking.query.get(booking_id)
    if not booking:
      return {"message": "Booking not found"}, 404
    
    if booking.service_id != professional.service_id:
      return {"message": "Unauthorized: This booking is not related to your registered service"}, 403
    

    if booking_status == "Accepted":
      booking.professional_id = professional.id
      booking.status="Accepted"   #status changes for only for accepted bookings
    
    elif booking_status=="Rejected":
      existing_rejection=Professional_rejected_bookings.query.filter_by(booking_id=booking.id, professional_id=professional.id).first()
      if not existing_rejection:
         rejected_booking = Professional_rejected_bookings(booking_id=booking.id, professional_id=professional.id)
         db.session.add(rejected_booking)
    
    try:
        db.session.commit()
        return {"message": f"Booking {booking_status} successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": "Failed to update booking", "error": str(e)}, 500
      
   
api.add_resource(ProfessionalBookings, '/professional/bookings', '/professional/bookings/update/<int:booking_id>')


class ProfessionalScheduledBookings(Resource):
  @jwt_required()
  def get(self):
    user_identity=get_jwt_identity()
    user_id=user_identity["id"]
    

    professional=Professional.query.filter_by(user_id=user_id).first()
    if not professional:
      return {"message": "Professional not found"},404
    
    bookings=Booking.query.filter_by(professional_id=professional.id,status="Accepted").all()

    scheduled_services=[{
      "id": booking.id,
      "customerName": booking.customer.user.username,
      "address": booking.customer.address,
      "phone": booking.customer.phone_no,
      "scheduledDate": booking.service_date.strftime("%Y-%m-%d"),
      "serviceName": booking.service.name,
      "status": booking.status,
    } for booking in bookings]
    return jsonify(scheduled_services)
  
  # @jwt_required()

  # def put(self, booking_id):
  #   print(f" PUT request received for Booking ID: {booking_id}") 
    
  
api.add_resource(ProfessionalScheduledBookings, '/professional/scheduled_bookings')


class ProfessionalServieHistory(Resource):
  @jwt_required()
  def get(self):
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]

    professional = Professional.query.filter_by(user_id=user_id).first()
    if not professional:
        return {"message": "Professional not found"}, 404

    # Fetch completed bookings with related customer and service details
    completed_services = Booking.query.filter_by(professional_id=professional.id, status="Completed").all()

    if not completed_services:
        return {"message": "No completed service found"}

    # Build response data
    booking_history = [
      {
        "booking_id": booking.id,
        "service_name": booking.service.name if booking.service else "Unknown",
        "customer_name": booking.customer.user.username if booking.customer else "Unknown",
        "customer_phone": booking.customer.phone_no if booking.customer else "Unknown",
        "customer_address": booking.customer.address if booking.customer else "Unknown",
        "service_date": booking.service_date.strftime("%Y-%m-%d"),
        "status": booking.status,
        "rating":booking.review[0].rating if booking.review else "Not Rated"
      }
      for booking in completed_services
    ]

    return jsonify({"completed_services": booking_history})


api.add_resource(ProfessionalServieHistory, "/servicehistory")


class ProfessionalStats(Resource):
  @jwt_required()
  def get(self):
    user_id=get_jwt_identity()["id"]

    user=User.query.get(user_id)
    if user.role!="professional":
      return {"message":"Access denaied: Professional Only"}
    
    try:
      professional = Professional.query.filter_by(user_id=user_id).first()
      if not professional:
        return {"message": "Professional profile not found"}, 404
      professional_id = professional.id
      service_id = professional.service_id
      new_service_request = Booking.query.filter_by(service_id=service_id, status="Pending").count()
      scheduled_services = Booking.query.filter_by(professional_id=professional_id, status="Accepted").count()
      rejected_bookings = Professional_rejected_bookings.query.filter_by(professional_id=professional_id).count()
      completed_services = Booking.query.filter_by(professional_id=professional_id, status="Completed").count() 
      professional_name = user.username 

      completed_bookings = Booking.query.filter_by(professional_id=professional_id, status="Completed").all()
      ratings = [booking.review[0].rating for booking in completed_bookings if booking.review]

      # Calculate average rating
      average_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0
    
    except Exception as e:
      return {"message": f"An error occurred: {str(e)}"}, 500

    return {
      "new_service_request":new_service_request,
      "scheduled_services":scheduled_services,
      "rejected_bookings":rejected_bookings,
      "completed_services": completed_services,
      "name":professional_name,
      "average_rating":average_rating
    },200

api.add_resource(ProfessionalStats, "/professionalstats")
      

class ExportClosedServices(Resource):
  @jwt_required()
  def post(self):
    current_user_email = get_jwt_identity()
    admin = User.query.filter_by(email=current_user_email, role="admin").first()

    if not admin:
      return {"message": "Unauthorized"}, 403
    
    # Trigger the Celery task
    # export_closed_services.delay(current_user_email)

    return {"message": "CSV export started. You will receive an email shortly."}, 200

api.add_resource(ExportClosedServices, "/export-closed-services")

class UserStats(Resource):
  def get(self):
    customers_count = Customer.query.count()
    professionals_count = Professional.query.count()
    return jsonify({
            "customers": customers_count,
            "professionals": professionals_count
        })
api.add_resource(UserStats, "/admin/user-stats")


class ServiceStats(Resource):
  def get(self):
    categories = Category.query.all()
    labels = [category.name for category in categories]
    counts = [len(category.services) for category in categories]
    return jsonify({"labels": labels, "counts": counts})

api.add_resource(ServiceStats, "/admin/service-stats") 

class BookingStatus(Resource):
  def get(self):
    statuses = ["Pending", "Ongoing", "Completed"]
    counts = [Booking.query.filter_by(status=status).count() for status in statuses]
    return jsonify({"labels": statuses, "counts": counts})
  
api.add_resource(BookingStatus, "/admin/booking-status")

class ProfessionalsPerService(Resource):
  def get(self):
      services = Service.query.all()
      labels = [service.name for service in services]
      counts = [len(service.professional_id) for service in services]
      return jsonify({"labels": labels, "counts": counts})

api.add_resource(ProfessionalsPerService, "/admin/professionals-per-service")

##############above code is for admin graphs#####################
    
class SearchServices(Resource):
  def get(self):
    service_name = request.args.get('service_name', '').strip()
    location = request.args.get('location', '').strip()

    query = Service.query

    # Filter by service name
    if service_name:
        query = query.filter(Service.name.ilike(f"%{service_name}%"))

    # Filter services based on professionals' location
    if location:
        service_ids = Professional.query.filter(
            Professional.address.ilike(f"%{location}%")
        ).with_entities(Professional.service_id).distinct()
        
        query = query.filter(Service.id.in_(service_ids))

    results = query.all()

    if not results:
        return {"message": "No services found"}, 200

    services = [
        {
            "id": service.id, 
            "service_name": service.name, 
            "description": service.description, 
            "base_price": service.base_price,
            "category_id": service.category_id  # <--- ✅ THIS IS THE FIX
        }
        for service in results
    ]
    return {"services": services}, 200

api.add_resource(SearchServices, "/searchservices")


#Admin search professionals by service and name
class SearchProfessionals(Resource):
  def get(self):
    name = request.args.get('name', '').strip()
    status = request.args.get('status', '').strip().lower()
    service_name = request.args.get('service_name', '').strip()
    max_rating = request.args.get('max_rating', '').strip()


    # Step 1: Get all approved users who are professionals
    approved_users = User.query.filter_by(approved=True, role="professional").all() 

    # Step 2: Filter professionals based on the approved users
    professionals = []
    for user in approved_users:
        professional = Professional.query.filter_by(user_id=user.id).first()  # Get the professional by user_id
        if professional:
            professionals.append(professional)

    user_data = []
    for professional in professionals:
        user = User.query.get(professional.user_id)  # Get the user details
        service = Service.query.get(professional.service_id)  # Get service details

        # Step 2: Filter by Name
        if name and not user.username.lower().startswith(name.lower()):
            continue

        # Step 3: Filter by Status
        if status:
            is_blocked = (status == "blocked")
            if user.is_blocked != is_blocked:
                continue

        # Step 4: Filter by Service Name
        if service_name and service and service_name.lower() not in service.name.lower():
            continue

        # Step 5: Get Completed Bookings Count
        completed_bookings = Booking.query.filter_by(professional_id=professional.id, status="Completed").count()

        # Step 6: Get Average Rating
        review_ratings = [
            review.rating for review in Review.query.filter(
                Review.booking_id.in_(
                    db.session.query(Booking.id).filter_by(professional_id=professional.id)
                )
            ).all()
        ]
        avg_rating = round(sum(review_ratings) / len(review_ratings), 1) if review_ratings else 0

        if max_rating:
          try:
            max_rating_value = float(max_rating)
            if avg_rating > max_rating_value:
              continue  # Skip professionals with a higher rating
          except ValueError:
            return jsonify({"error": "Invalid rating value"}), 400


        # Step 7: Append professional details
        user_data.append({
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "status": "Blocked" if user.is_blocked else "Unblocked",
            "service": service.name if service else "Not Assigned",
            "completed_bookings": completed_bookings,
            "rating": avg_rating if avg_rating > 0 else 0
        })

    return jsonify({"professionals": user_data})  

api.add_resource(SearchProfessionals, "/searchprofessionals")


class Profile(Resource):
    @jwt_required()
    def get(self):
        """Fetch user profile based on role."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        profile_data = {
            "fullName": user.username,  
            "email": user.email,
            "role": user.role, 
        }

        if user.role == "customer":
            customer = Customer.query.filter_by(user_id=user.id).first()
            if customer:
                profile_data.update({
                    "phone": customer.phone_no,
                    "address": customer.address,
                })
        elif user.role == "professional":
            professional = Professional.query.filter_by(user_id=user.id).first()
            if professional:
                profile_data.update({
                    "phone": professional.phone_no,
                    "address": professional.address,
                })

        return profile_data, 200

    @jwt_required()
    def put(self):
        """Update user profile based on role."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()
        full_name = data.get("fullName", "").strip()
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()

        if not full_name or not phone or not address:
            return {"error": "Full Name, Phone, and Address are required fields"}, 400

        user.username = full_name  # Allow name update

        if user.role == "customer":
            customer = Customer.query.filter_by(user_id=user.id).first()
            if customer:
                customer.phone_no = phone
                customer.address = address
        elif user.role == "professional":
            professional = Professional.query.filter_by(user_id=user.id).first()
            if professional:
                professional.phone_no = phone
                professional.address = address

        try:
            db.session.commit()
            return {"message": "Profile updated successfully!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to update profile", "details": str(e)}, 500

api.add_resource(Profile, "/profile")


@api_blueprint.route('/create-csv')
def createCSV():
    task = export_closed_service_requests_csv.delay()
    return jsonify({'task_id': task.id}), 200


@api_blueprint.route('/get-csv-data/<task_id>')
def getCSV(task_id):
    result = AsyncResult(task_id)

    if result.ready():
        file_path = result.result

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True), 200
        else:
            return jsonify({"error": "File not found"}), 404
    else:
        return jsonify({"message": "Task is not ready"}), 405
