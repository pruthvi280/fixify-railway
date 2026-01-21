from flask import Blueprint, request, flash, redirect, url_for, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with, Api
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Professional,Customer,Service
from .database import db
import os
from datetime import timedelta



authorizarion=Blueprint('authorization',__name__)

signup_parser=reqparse.RequestParser()
signup_parser.add_argument("name",type=str,help='Username is required',required=True)
signup_parser.add_argument("email",type=str,help='Email is required',required=True)
signup_parser.add_argument("password",type=str,help='Password is required',required=True)
signup_parser.add_argument("role",type=str,help='Role (customer or professional) is required',required=True)
signup_parser.add_argument("phone", type=str, help="Phone number is required", required=False)
signup_parser.add_argument("address", type=str, help="Address is required", required=False)
signup_parser.add_argument("document", type=str, help="Document is required for professionals", required=False)
signup_parser.add_argument("service", type=str, help="Service  is required for professionals", required=False)


user_fields={
  "user_id":fields.Integer,
  "username":fields.String,
  "email":fields.String,
  "role":fields.String,
  "token":fields.String
}


class SignUp(Resource):
  @marshal_with(user_fields)
  def post(self):
    username = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmPassword")
    role = request.form.get("role")
    phone_no = request.form.get("phone")
    address = request.form.get("address")
    service = request.form.get("service")
    
    if role not in ["customer", "professional"]:
      abort(400,message='Invalid role.The role should be either professional or customer')
    
    user=User.query.filter_by(email=email).first()
    if user:
      abort(409,message="Email is already exists.")

    if role == "customer":
        approved = True  # Customers are automatically approved
    else:
        approved = False  # Professionals need admin approval, so initially set to False
    
    

    # If role is customer, create a Customer record
    if role == "customer":
      new_customer = Customer(phone_no=phone_no, address=address)
      new_user=User(
        username=username,
        email=email,
        password=generate_password_hash(password,method='scrypt'),
        role=role,
        approved=approved,
        customer_dets = new_customer,
      )

      db.session.add(new_user)
      db.session.commit()
    
      token_access=create_access_token(
          identity=user,
          expires_delta=timedelta(hours=3)
      )

      response = {
        "user_id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "token": token_access,
        "role": new_user.role,
        "approved": new_user.approved
      }
      return response, 201

    # If role is professional, create a Professional record
    elif role == "professional":

      from flask import current_app
      UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER', '/app/storage/uploads') 
      os.makedirs(UPLOAD_FOLDER, exist_ok=True)

      # Handle file upload
      if "document" not in request.files:
          return {"message": "No document uploaded"}, 400

      file = request.files["document"]
      if file.filename == "":
          return {"message": "No file selected"}, 400

      file_path = os.path.join(UPLOAD_FOLDER, file.filename)
      file.save(file_path)

        # Validate service_id if provided
      path = file.filename
      if service:
          service = Service.query.filter_by(name = service).first()
          print(service)
          if not service:
            abort(400, message="Invalid service .")

      new_professional = Professional(
          phone_no=phone_no,
          address=address,
          document=path,
          service=service
      )
      new_user=User(
        username=username,
        email=email,
        password=generate_password_hash(password,method='scrypt'),
        role=role,
        approved=approved,
        Professional_dets = new_professional
      )

      db.session.add(new_user)
      db.session.commit()  # Commit all changes

    

      response={
        "user_id":new_user.id,
        "username":new_user.username,
        "email":new_user.email,
        # "token":token_access,
        "role":new_user.role,
        "approved": new_user.approved
      }
      
      return response,201
  
login_parser=reqparse.RequestParser()
login_parser.add_argument("email",type=str,help='This field is mandatory to fill',required=True)
login_parser.add_argument("password",type=str,help="This field is mandatory to fill",required=True)

login_fields={
  "user_id":fields.Integer,
  "username":fields.String,
  "email":fields.String,
  "role":fields.String,
  "token":fields.String,
  "approved": fields.Boolean 
  }


class Login(Resource):
    def post(self):
        req_args = login_parser.parse_args()
        email = req_args["email"]
        password = req_args["password"]

        print(f"🔍 Login attempt: Email={email}, Password={password}")


        user = User.query.filter_by(email=email).first()
        print(f"🔍 User found: {user}")

        if not user:
            abort(401, description="User does not exist")

        if user.is_blocked:
            return {"blocked": True, "message": "User is blocked"}, 200

        if not check_password_hash(user.password, password):
            abort(403, description="Incorrect Password")

        if user.role == "professional" and not user.approved:
            return {"approved": False, "message": "User is not approved yet"}, 200

        # Generate JWT Token
        token_access = create_access_token(
            identity=user,
            expires_delta=timedelta(hours=3)
        )

        response = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "token": token_access,
            "approved": user.approved,
            "blocked": False
        }

        return response, 200


blacklist=set()

class Logout(Resource):
  @jwt_required()
  def post(self):
    jti=get_jwt()["jti"]
    print(jti)
    blacklist.add(jti)

    return {"message":"Your are logged out successfully"},200
  



class Ping(Resource):
    def get(self):
        return {"message": "Backend is alive"}, 200
