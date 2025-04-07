




import hmac
import hashlib
import base64
import os
import logging
import re

from retail_app.config.config import Config
from retail_app.commonutil.commonutil_service import CommonJsonResponse
from retail_app.db_service.db_common_service import DBService
from retail_app.db_service.models import UserAuth,Customer
from retail_app.commonutil.commonutil_service import validationService
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
import base64
import json
import uuid
import time
import random
import datetime
import jwt

from retail_app.commonutil.commonutil_service import EncryptDecryptService
from retail_app.commonutil.commonutil_service import EmailService
from retail_app.commonutil.jwt_service import JwtServiceImpl
from retail_app.service import redis_client

class TokenService:

    
    def generate_otp(self,phone,interval=300):
        """Generate OTP using HMAC-SHA256 (Reproducible)"""
        otp = str(random.randint(100000, 999999))
        payload = {
            "phone": phone,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=interval)
        }
        otp_token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
        redis_client.setex(f"otp:{otp_token}", interval, otp)
        return {
            "otp_token": otp_token,
            "expires_in": interval,
            "otp": otp
        } 
            

    def verify_otp(self,otp_token):
        try:
            payload = jwt.decode(otp_token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'status':False,"message":"OTP has been expired"}
        except jwt.InvalidTokenError:
            return {'status':False,"message":"Invalid Token"}
           
        stored_otp = redis_client.get(f"otp:{otp_token}")
        return {'status':'SUCCESS','otp':stored_otp}
    
    
    
class OtpCreation:

    def __init__(self):

        self.validate = validationService()
        self.otp = TokenService()
        self.enc_obj = EncryptDecryptService()

    def get_otp(self,request):
        """
        Otp creation for signup.
        """

        logging.info(f"Request for otp creation")
          
        if not all([request.email, request.phone]):
                return CommonJsonResponse.common_response(
                    message="All fields are required",
                    status_code=400
                )
        
        if not self.validate.validate_email(request.email):
            return CommonJsonResponse.common_response(
                message="Invalid email format",
                status_code=400
            )

        if not self.validate.validate_phone(request.phone):
            return CommonJsonResponse.common_response(
                message="Invalid phone number format",
                status_code=400
            )is None
        
        existing_customer = DBService.find_one(UserAuth, {"username": request.email}, is_mongo=False)
                                        
        logging.info(f"existing_customer: {existing_customer}")
        if existing_customer:
                return CommonJsonResponse.common_response(
                    message="User already exists",
                    status="success"  
                )
        try:
            # login_id = str(uuid.uuid4())
            auth_data={
                    "username": request.email
                    }
            auth_insert = DBService.create_record(UserAuth,auth_data,is_mongo=False)
            
        except Exception as e:
                logging.exception(f"Exception triggered in the auth details insertion:{e}")
                print("kkkk")

        print("auth_insert",auth_insert)
        try:
            cust_data = {
                "email": request.email,
                "phone": request.phone,
                "login_id":auth_insert.login_id 
            }
              
            new_customer = DBService.create_record(Customer,cust_data,is_mongo=False)
           

        except Exception as e:
            logging.exception(f"Exception triggered in the customer details insertion:{e}")

        otp = self.otp.generate_otp(request.phone)
    
       
        try:
            email_sent = EmailService.send_email(
                subject="OTP for account creation",
                recipients=[request.email],
                body=f"OTP for account creation is: {otp.get('otp')}"
            )
        except Exception as e:
            print("Error sending email:", e)
            email_sent = False
        
        if not email_sent:
            return CommonJsonResponse.common_response("failure",
                message="User registration failed - Unable to send email",
                status_code=500
            )

        resp_dict = {
                    "username" : request.email,
                    "login_id" : auth_insert.login_id,
                    "otp_token":otp.get('otp_token'),
                    "expires_in":otp.get('expires_in')
                    }

        # enc_obj = EncryptDecryptService()
        print("resp_dict", resp_dict)       

        encrypt_resp = self.enc_obj.encrypt_aes_gcm(resp_dict)
        
        return CommonJsonResponse.common_response(
            "SUCCESS",
            "Otp sent to the email.",
            data = encrypt_resp,
            status_code=201
        )
        
class OtpVerification:
     
    def __init__(self):
        self.validate = validationService()
        self.otp = TokenService()
        self.enc_obj = EncryptDecryptService()

    def otp_verification(self,request):
        """
        Otp verification for signup
        """
        logging.info(f"Request for otp creation")

        if not all([request.login_id, request.otp_token,request.otp]):
                return CommonJsonResponse.common_response(
                    message="All fields are required",
                    status_code=400
                )

        # if not self.validate.validate_email(request.email):
        #     return CommonJsonResponse.common_response(
        #         message="Invalid email format",
        #         status_code=400
        #     )

        # if not self.validate.validate_phone(request.phone):
        #     return CommonJsonResponse.common_response(
        #         message="Invalid phone number format",
        #         status_code=400
        #     )
        existing_customer = DBService.find_one(UserAuth, {"login_id": request.login_id}, is_mongo=False)
        logging.info(f"existing_customer: {existing_customer}")
        if not  existing_customer:
                return CommonJsonResponse.common_response(
                    message="User does not exists",
                    status="FAILURE"  
                )
        try:
            stored_otp = self.otp.verify_otp(request.otp_token)
            print("stored_otp", stored_otp)
            
            if stored_otp['status']!= "SUCCESS":
                redis_client.delete(request.otp_token)
                return CommonJsonResponse.common_response(
                    message=stored_otp['message'],
                    status_code=400,
                    status = "FAILURE"
                )
           
            if stored_otp['otp'] != request.otp:
                  return CommonJsonResponse.common_response(
                    message="Invalid OTP",
                    status_code=400,
                    status = "FAILURE"
                )
            
            redis_client.delete(request.otp_token)

            resp_dict = {}

            encrypt_resp = self.enc_obj.encrypt_aes_gcm(resp_dict)
            
            return CommonJsonResponse.common_response(
                "SUCCESS",
                "Successfully verify the otp.",
                data = encrypt_resp,
                status_code=201
            )
        
        except Exception as e:
            logging.exception(f"Exception triggere in OTP verification:{e}")

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
                 
                 
class AccountCreation:
     
    def __init__(self):
        self.enc_obj = EncryptDecryptService()
        self.jwt = JwtServiceImpl()
    
    def account_creation(self, request):
        """
        Account creation for signup
        """
        logging.info(f"Request for account creation")

        if not all([request.login_id,request.password]):
                return CommonJsonResponse.common_response(
                    message="All fields are required",
                    status_code=400
                )
        
        existing_customer = DBService.find_one(UserAuth, {"login_id": request.login_id}, is_mongo=False)
        logging.info(f"existing_customer: {existing_customer}")

        if not  existing_customer:
                return CommonJsonResponse.common_response(
                    message="User does not exists",
                    status="FAILURE"  
                )
        hash_pwd = bcrypt.generate_password_hash(request.password).decode('utf-8')

        update_login = DBService.update_record(UserAuth, {"login_id": request.login_id}, {"password":hash_pwd}, is_mongo=False)
        
        tokens = self.jwt.generate_jwt_tokens(request.login_id)

        resp_dict = {
                    "access_token": tokens.get('access_token'),
                    "refresh_token": tokens.get('refresh_token'),
                    "token_type":tokens.get('token_type'),
                    "login_id":request.login_id
                    }
        
        encrypt_resp = self.enc_obj.encrypt_aes_gcm(resp_dict)
        
        return CommonJsonResponse.common_response(
             "SUCCESS",
            "Successfully created the account.",
            data = encrypt_resp,
            status_code=201
        
                                                    )




        

        




