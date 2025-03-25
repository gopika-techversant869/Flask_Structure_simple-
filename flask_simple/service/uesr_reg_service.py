
from flask import jsonify
from flask_simple.db_service.models import Customer,UserAuth
from flask_simple.db_service.db import db
from flask_simple.db_service.db_common_service import DBService
from flask_simple.config.config import Config
import datetime
from flask_simple.commonutil.commonutil_service import CommonJsonResponse
from flask_bcrypt import Bcrypt
import logging



from flask_bcrypt import Bcrypt

bcrypt = Bcrypt() 

class UserRegisterServiceImpl:
    def register_user(self, data):  
        

        logging.info("Before processing Req:",data)
        existing_customer = DBService.find_one(Customer, {"email": data.user_email}, is_mongo=False)

        if existing_customer:
            return CommonJsonResponse.common_response(message="User already exists", status_code=200)

        pwd = "admin@123"
        hash_pwd = bcrypt.generate_password_hash(pwd).decode('utf-8')
        print("heashed one",hash_pwd)

        cust_data = {
            "name": data.name,  
            "email": data.user_email,
            "phone": data.phone,
            "address": data.address
        }
        
        new_customer = DBService.create_record(Customer, cust_data, is_mongo=False)
        
        try:

            auth_data = {
                "customer_id": new_customer.id,
                "role": data.role if data.role else "user"  
            }

            auth_insert = DBService.create_record(UserAuth, auth_data, is_mongo=False)
        except Exception as e:
            logging.info("Error",e)

        return CommonJsonResponse.common_response("SUCCESS", "User registered successfully", status_code=201)
