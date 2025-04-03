from retail_app.db_service.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import uuid
import datetime


# class User(db.Model):
#     login_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  
#     failed_attempts = db.Column(db.Integer, default=0) 

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

def generate_uuid():
    return str(uuid.uuid4()) 

class UserAuth(db.Model):
    __tablename__ = 'user_auth' 
    
    login_id = db.Column(db.String(36), primary_key=True, default=generate_uuid())  
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")
    is_active = db.Column(db.Boolean, default=True)
    login_attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime)


    customers = db.relationship('Customer', back_populates='user_auth')  

class Customer(db.Model):
    __tablename__ = 'customer'  

    customer_id = db.Column(db.String(36), primary_key=True, default=generate_uuid())  
    login_id = db.Column(db.String(36), db.ForeignKey('user_auth.login_id'), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

   
    user_auth = db.relationship('UserAuth', back_populates='customers')  




class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)


# class Products(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     category = db.Column(db.String(50), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     stock_quantity = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
