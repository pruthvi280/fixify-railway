from .database import db
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    approved = db.Column(db.Boolean(), default=False)
    is_blocked = db.Column(db.Boolean(), default=False)
    role = db.Column(db.String(20), nullable = False)
    # is_deleted = db.Column(db.String(20), nullable = False)
    customer_dets = db.relationship('Customer', backref='user', cascade='all, delete',  lazy=True, uselist=False)
    Professional_dets=db.relationship('Professional',backref='user', cascade='all, delete', lazy=True, uselist=False)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    phone_no=db.Column(db.String(10),unique=True)
    address = db.Column(db.String(100), nullable=False)
    booking = db.relationship('Booking', backref='customer', lazy=True)


class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)    
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    address = db.Column(db.String(100), nullable=False)
    phone_no=db.Column(db.String(10),unique=True)
    document=db.Column(db.String(120),nullable=False)
    service_id=db.Column(db.Integer,db.ForeignKey('service.id'))
    booking = db.relationship('Booking', backref='professional', lazy=True)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    booking = db.relationship('Booking', backref='service', lazy=True)
    professional_id = db.relationship('Professional', backref='service', lazy=True)
    # incentive=db.Column(db.Float,nullable=True,default=0.0)
    

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    status = db.Column(db.String(30), default='Pending')
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)
    service_date=db.Column(db.DateTime,default=datetime.now)
    
    review = db.relationship("Review", backref="booking", lazy= True)


class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(150), nullable=False, unique=True)
    # image = db.Column(db.String, nullable= True)
    services=db.relationship("Service",backref="category",lazy=True)

        

class Review(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    booking_id=db.Column(db.Integer,db.ForeignKey('booking.id'),nullable=False)
    feedback=db.Column(db.Text,nullable=False)
    rating=db.Column(db.Integer,nullable=False)


class Professional_rejected_bookings(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    booking_id=db.Column(db.Integer,db.ForeignKey('booking.id'),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey('professional.id'),nullable=False)

class Payment(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    booking_id=db.Column(db.Integer,db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="Completed")
    transaction_date = db.Column(db.DateTime, default=datetime.now)
    booking = db.relationship('Booking', backref='payment', lazy=True)
    

