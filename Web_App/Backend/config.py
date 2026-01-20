import os

class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret")

    # Database (Uses the permanent volume via Railway Variable)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///house_hold_service.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

    # Celery
    CELERY = {
        "broker_url": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        "result_backend": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        "task_ignore_result": True,
    }

    # Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # ✅ NEW: Save Resumes to the Permanent Volume
    UPLOAD_FOLDER = "/app/storage/uploads"
