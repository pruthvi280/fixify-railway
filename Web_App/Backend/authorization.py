from flask import Blueprint, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Professional, Customer, Service
from .database import db
import os
from datetime import timedelta

authorizarion = Blueprint("authorization", __name__)

# -------------------- SIGNUP --------------------

user_fields = {
    "user_id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "role": fields.String,
    "token": fields.String,
}

class SignUp(Resource):
    @marshal_with(user_fields)
    def post(self):
        username = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        phone_no = request.form.get("phone")
        address = request.form.get("address")
        service_name = request.form.get("service")

        if role not in ["customer", "professional"]:
            abort(400, message="Invalid role")

        if User.query.filter_by(email=email).first():
            abort(409, message="Email already exists")

        approved = True if role == "customer" else False

        # ---------------- CUSTOMER SIGNUP ----------------
        if role == "customer":
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method="scrypt"),
                role="customer",
                approved=True,
            )

            db.session.add(new_user)
            db.session.commit()  # get new_user.id

            new_customer = Customer(
                user_id=new_user.id,
                phone_no=phone_no,
                address=address,
            )

            db.session.add(new_customer)
            db.session.commit()

            token = create_access_token(
                identity=new_user,
                expires_delta=timedelta(hours=3),
            )

            return {
                "user_id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "role": new_user.role,
                "token": token,
            }, 201

        # ---------------- PROFESSIONAL SIGNUP ----------------
        from flask import current_app

        UPLOAD_FOLDER = current_app.config.get(
            "UPLOAD_FOLDER", "/app/storage/uploads"
        )
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if "document" not in request.files:
            abort(400, message="No document uploaded")

        file = request.files["document"]
        if file.filename == "":
            abort(400, message="No file selected")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        service = None
        if service_name:
            service = Service.query.filter_by(name=service_name).first()
            if not service:
                abort(400, message="Invalid service")

        new_professional = Professional(
            phone_no=phone_no,
            address=address,
            document=file.filename,
            service=service,
        )

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method="scrypt"),
            role="professional",
            approved=False,
            Professional_dets=new_professional,
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
        }, 201


# -------------------- LOGIN --------------------

login_parser = reqparse.RequestParser()
login_parser.add_argument("email", type=str, required=True)
login_parser.add_argument("password", type=str, required=True)

class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        email = args["email"]
        password = args["password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            abort(401, message="User does not exist")

        if user.is_blocked:
            return {"blocked": True, "message": "User is blocked"}, 200

        if not check_password_hash(user.password, password):
            abort(403, message="Incorrect password")

        if user.role == "professional" and not user.approved:
            return {"approved": False, "message": "Not approved"}, 200

        token = create_access_token(
            identity=user,
            expires_delta=timedelta(hours=3),
        )

        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "token": token,
            "approved": user.approved,
        }, 200


# -------------------- LOGOUT --------------------

blacklist = set()

class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Logged out successfully"}, 200


# -------------------- PING --------------------

class Ping(Resource):
    def get(self):
        return {"message": "Backend is alive"}, 200

