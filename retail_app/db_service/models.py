from retail_app.db_service.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import uuid


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
    return str(uuid.uuid4())  # Generates a unique string-based UUID

class Customer(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)  
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)

    user_auth = db.relationship("UserAuth", backref="customer", uselist=False, cascade="all, delete-orphan")

class UserAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing PK for auth
    customer_id = db.Column(db.String(36), db.ForeignKey("customer.id"), unique=True, nullable=False)  # FK uses UUID
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # "admin" or "user"
    login_attempts = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password = Bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return Bcrypt.check_password_hash(self.password, password)
