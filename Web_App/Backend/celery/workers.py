from Backend import create_app
from Backend.celery.celery_factory import celery_init_app

# Create Flask app
app = create_app()

# Initialize Celery with Flask app
celery_app = celery_init_app(app)

# Import scheduled tasks AFTER app context is ready
with app.app_context():
    import Backend.celery.celery_scheduled
