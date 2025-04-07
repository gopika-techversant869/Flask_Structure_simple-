
# from flask import jsonify
# from flask_simple.db_service.models import Customer,UserAuth
# from flask_simple.db_service.db import db
# from flask_simple.db_service.db_common_service import DBService
# from flask_simple.config.config import Config
# import datetime
# from flask_simple.commonutil.commonutil_service import CommonJsonResponse
# from flask_bcrypt import Bcrypt
# import logging



# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt() 

# class UserRegisterServiceImpl:
#     def register_user(self, data):  
        

#         logging.info("Before processing Req:",data)
#         existing_customer = DBService.find_one(Customer, {"email": data.user_email}, is_mongo=False)

#         if existing_customer:
#             return CommonJsonResponse.common_response(message="User already exists", status_code=200)

#         pwd = "admin@123"
#         hash_pwd = bcrypt.generate_password_hash(pwd).decode('utf-8')
#         print("heashed one",hash_pwd)

#         cust_data = {
#             "name": data.name,  
#             "email": data.user_email,
#             "phone": data.phone,
#             "address": data.address
#         }
        
#         new_customer = DBService.create_record(Customer, cust_data, is_mongo=False)
        
#         try:

#             auth_data = {
#                 "customer_id": new_customer.id,
#                 "role": data.role if data.role else "user"  
#             }

#             auth_insert = DBService.create_record(UserAuth, auth_data, is_mongo=False)
#         except Exception as e:
#             logging.info("Error",e)

#         return CommonJsonResponse.common_response("SUCCESS", "User registered successfully", status_code=201)

from flask import jsonify
from retail_app.db_service.models import Customer, UserAuth
from retail_app.db_service.db import db
from retail_app.db_service.db_common_service import DBService
import datetime
from retail_app.commonutil.commonutil_service import CommonJsonResponse
from retail_app.commonutil.commonutil_service import PasswordGenerator,EmailService,EncryptDecryptService
from flask_bcrypt import Bcrypt
import logging
import re
from sqlalchemy.exc import SQLAlchemyError
import secrets
import string
import os
from werkzeug.security import generate_password_hash

from retail_app.commonutil.commonutil_service import PasswordGenerator,EmailService,EncryptDecryptService
from flask_bcrypt import Bcrypt
import logging
import re
from sqlalchemy.exc import SQLAlchemyError
import secrets
import string
import os

bcrypt = Bcrypt()


class UserRegisterServiceImpl:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        
    def validate_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def validate_phone(self, phone):
        phone_pattern = r'^\d{10}$'
        return re.match(phone_pattern, phone) is not None

    def register_user(self, data):
        try:
            self.logger.info(f"Processing registration request for email: {data.user_email}")

        
            if not all([data.name, data.user_email, data.phone]):
                return CommonJsonResponse.common_response(
                    message="All fields are required",
                    status_code=400
                )

            if not self.validate_email(data.user_email):
                return CommonJsonResponse.common_response(
                    message="Invalid email format",
                    status_code=400
                )

            if not self.validate_phone(data.phone):
                return CommonJsonResponse.common_response(
                    message="Invalid phone number format",
                    status_code=400
                )

            existing_customer = DBService.find_one(
                Customer,
                {"email": data.user_email},
                is_mongo=False
            )

            if existing_customer:
                return CommonJsonResponse.common_response(
                    message="User already exists",
                    status="success"
                    
                )

            obj = PasswordGenerator()
            temp_password = obj.generate_secure_password()
            print("password:",temp_password)
            # hash_pwd = generate_password_hash(temp_password)
            hash_pwd = bcrypt.generate_password_hash(temp_password).decode('utf-8')
            try:
                auth_data = {
                        "password": hash_pwd,
                        "role": data.role if hasattr(data, 'role') else "user",
                        "login_attempts": 0,
                        "is_active": True,
                        "username": data.user_email
                    }
                    
                auth_insert = DBService.create_record(
                    UserAuth,
                    auth_data,
                    is_mongo=False
                )
            except Exception as e:
                print("exception triggered", e)
            
            try:
                mongo_login = DBService.create_record(UserAuth,auth_data,is_mongo=True)
            except Exception as e:
                print("exception triggered",e)
          
            try:
                cust_data = {
                    "name": data.name,
                    "email": data.user_email,
                    "phone": data.phone,
                    "address": data.address,
                    
                }
                 
                new_customer = DBService.create_record(Customer,cust_data,is_mongo=False)
                print("new customer",new_customer)
                print("type",type(data.name))
                try:
                    cust_data['customer_id'] = new_customer.customer_id
                    mongo_data = DBService.create_record(Customer, cust_data, is_mongo=True)
                except Exception as e:
                    print("Error",e)

               
                
              
                try:
                    email_sent = EmailService.send_email(
                        subject="Your Temporary Password",
                        recipients=[data.user_email],
                        body=f"Your temporary password is: {temp_password}"
                    )
                except Exception as e:
                    print("Error sending email:", e)
                    email_sent = False
                
                if not email_sent:
                    return CommonJsonResponse.common_response("failure",
                        message="User registration failed - Unable to send email",
                        status_code=500
                    )

                self.logger.info(f"Successfully registered user: {data.user_email}")

                resp_dict = {
                            "login_id":"",
                            "user_name":""}
                enc_obj = EncryptDecryptService()
                
                encrypt_resp = enc_obj.encrypt_aes_gcm(resp_dict)
                print("encrypt_resp",encrypt_resp)
                
                return CommonJsonResponse.common_response(
                    "SUCCESS",
                    "User registered successfully. Please check your email for temporary password.",
                    data = encrypt_resp,
                    status_code=201
                )

            except SQLAlchemyError as e:
                db.session.rollback()
                self.logger.error(f"Database error during registration: {str(e)}")
                return CommonJsonResponse.common_response(
                    message=f"Registration failed due to database error:{str(e)}",
                    status_code=500
                )

        except Exception as e:
            self.logger.error(f"Unexpected error during registration: {str(e)}")
            return CommonJsonResponse.common_response(
                message="Registration failed due to unexpected error",
                status = "Failure"
            )








