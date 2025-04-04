




import hmac
import hashlib
import base64
import os
import logging
import re

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

from retail_app.commonutil.commonutil_service import EncryptDecryptService


class TokenService:

    def generate_otp_token(self):
        """Generate a random OTP token (sent to UI)"""
        return base64.urlsafe_b64encode(os.urandom(16)).decode()

    def generate_otp(self,otp_token,interval=30):
        """Generate OTP using HMAC-SHA256 (Reproducible)"""
        SECRET_KEY = "123"  
        secret_key = SECRET_KEY
        timestamp = int(time.time())
        time_slice = timestamp // interval
        time_bytes = time_slice.to_bytes(8, byteorder='big')
        
        hmac_obj = hmac.new(
            base64.b32decode(secret_key),
            time_bytes,
            hashlib.sha256
        )
        hmac_result = hmac_obj.hexdigest()
        offset = int(hmac_result[-1], 16)
        otp_hex = hmac_result[offset:offset+8]
        otp_decimal = int(otp_hex, 16) & 0x7fffffff
        otp = str(otp_decimal)[-6:].zfill(6)
        return otp
    
    def verify_totp(self, otp_to_verify, interval=30, valid_window=1):
        """
        Verify the provided TOTP
        """
        for i in range(-valid_window, valid_window + 1):
            current_time = int(time.time()) + (i * interval)
            if self.generate_totp(interval) == str(otp_to_verify):
                return True
        return False
    
class OtpCreation:

    def __init__(self):

        self.validate = validationService()
        self.otp = TokenService()
    def get_otp(self,request):
        """
        Otp creation for signup.
        """
        
        logging.info(f"Request for otp creation")

        if not all([request.name, request.email, request.phone_number]):
                return CommonJsonResponse.common_response(
                    message="All fields are required",
                    status_code=400
                )

        if not self.validate.validate_email(request.user_email):
            return CommonJsonResponse.common_response(
                message="Invalid email format",
                status_code=400
            )

        if not self.validate.validate_phone(request.phone):
            return CommonJsonResponse.common_response(
                message="Invalid phone number format",
                status_code=400
            )
        existing_customer = DBService.find_one(UserAuth,{'login_id':1},join_table=Customer,join_field='login_id')
        logging.info(f"existing_customer: {existing_customer}")
        if existing_customer:
                return CommonJsonResponse.common_response(
                    message="User already exists",
                    status="success"  
                )
        try:
            login_id = str(uuid.uuid4())
            auth_data={
                    "username": request.email,
                    "login_id":login_id}
            auth_insert = DBService.create_record(UserAuth,auth_data,is_mongo=False)
        except Exception as e:
                logging.exception(f"Exception triggered in the auth details insertion:{e}")
        try:
            cust_data = {
                "name": request.name,
                "email": request.email,
                "phone": request.phone,
                "address": request.address,
                "login_id":auth_insert.login_id 
            }
                
            new_customer = DBService.create_record(Customer,cust_data,is_mongo=False)

        except Exception as e:
            logging.exception(f"Exception triggered in the customer details insertion:{e}")

        otp_token = self.otp.generate_otp_token()
        otp = self.otp.generate_otp(otp_token)

        resp_dict = {
                    "username" : request.username,
                    "login_id" : login_id
                    }

        enc_obj = EncryptDecryptService()       

        encrypt_resp = enc_obj.encrypt_aes_gcm(resp_dict)
        
        return CommonJsonResponse.common_response(
            "SUCCESS",
            "Otp sent to the email.",
            data = encrypt_resp,
            status_code=201
        )
        
class OtpVerification:
     
    def __init__(self):
          pass

    def otp_verification(self,request):
        """
        Otp verification for signup
        """



               
        
        


