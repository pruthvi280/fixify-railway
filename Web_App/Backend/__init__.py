# Backend/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from .database import db
from .cache import cache
from .models import User
from .api import api_blueprint
from . import flask_mail
from .config import Config
import os  # <--- Make sure this is imported

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)

    # ✅ NEW: Create the permanent upload folder immediately
    # This prevents the "File Not Found" error when professionals sign up.
    upload_folder = app.config.get('UPLOAD_FOLDER', '/app/storage/uploads')
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder)
            print(f"✅ Created permanent upload folder at: {upload_folder}")
        except Exception as e:
            print(f"❌ Error creating upload folder: {e}")

    db.init_app(app)
    CORS(app)
    cache.init_app(app)
    flask_mail.mail.init_app(app)

    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity["id"]).one_or_none()

    # from .views import views
    from .authorization import authorizarion

    # app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(authorizarion, url_prefix="/")
    app.register_blueprint(api_blueprint, url_prefix="/")

    with app.app_context():
        db.create_all()

        user = User.query.filter_by(email="admin@gmail.com").first()
        if not user:
            admin_user = User(
                username="admin",
                email="admin@gmail.com",
                password=generate_password_hash("1234", method="scrypt"),
                role="admin",
                approved=True,
                is_blocked=False
            )
            db.session.add(admin_user)
            db.session.commit()

    return app