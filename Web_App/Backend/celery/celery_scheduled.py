from celery.schedules import crontab,timedelta
from flask import current_app as app
from Backend.celery.tasks import pending_bookings_reminder,send_monthly_activity_report

celery_app=app.extensions['celery']



@celery_app.on_after_configure.connect
def setup_periodic_task2(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/5'),
        pending_bookings_reminder.s(),
    )

@celery_app.on_after_configure.connect
def setup_periodic_tasks3(sender, **kwargs):
    
    sender.add_periodic_task(
        (50000000),  # Approximately every 30 days
        send_monthly_activity_report.s(),
    )

