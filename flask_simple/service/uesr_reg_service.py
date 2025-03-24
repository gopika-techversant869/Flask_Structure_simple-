
from flask import jsonify
from flask_simple.db_service.models import Customer,UserAuth
from flask_simple.db_service.db import db
from flask_simple.db_service.db_common_service import DBService
from flask_simple.config.config import Config
import datetime
from flask_simple.commonutil.commonutil_service import CommonResponse
from flask_bcrypt import Bcrypt




class UserRegisterServiceImpl:


   def register_user(self,data):
        existing_customer = DBService.find_one(Customer,{"email":data['user_email']},is_mongo=False)

        if existing_customer:
            return CommonResponse.create_response("FAILURE","User already exist",status_code=400)
        

        pwd = "admin@123"
        hash_pwd =  Bcrypt.generate_password_hash(pwd).decode('utf-8')

        cust_data = {
                    "name" : data.get["name"],
                    "email" : data.get["email"],
                    "phone" : data.get("phone"),
                    "address" : data.get("address")
                    }
        
        new_customer = DBService.create_record(Customer,cust_data,is_mongo=False)

        auth_data = {
                    "customer_id":new_customer.id,
                    "role" : data.get("role")
                    }

        auth_insert = DBService.create_record(UserAuth,auth_data,is_mongo=False)

        return CommonResponse.create_response("SUCCESS","User registered successfully",status_code=201)
