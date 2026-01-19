# main.py

from Backend import create_app
from Backend.database import db
from flask import send_from_directory
import os
from Backend.celery.celery_factory import celery_init_app
import flask_excel as excel  

#  Initialize Flask App
app = create_app()

#  Configure Celery
app.config["CELERY"] = {
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/1",
    "timezone": "Asia/Kolkata",
}
celery_app = celery_init_app(app)


with app.app_context():  
    import Backend.celery.celery_scheduled


UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


excel.init_excel(app)


if __name__ == "__main__":
    app.run(debug=True)
