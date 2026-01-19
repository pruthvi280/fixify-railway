class Config:
    SECRET_KEY = "my_secret_key"
    JWT_SECRET_KEY = "super_secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///house_hold_service.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]
    
    # # Mail Configuration
    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 465
    # MAIL_USERNAME = "pruthviprasad280@gmail.com"  # Change it from your mail id
    # MAIL_PASSWORD = "ieyy glbe escr dmib"  # Change the password accordingly.
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    
    

