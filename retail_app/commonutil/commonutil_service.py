

from typing import Optional, Union, Dict, Any, Tuple
from flask import jsonify
from http import HTTPStatus
import datetime
import uuid
import secrets
import string
from flask_mail import Message
from retail_app.extensions import mail
from retail_app.config.config import Config

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
import base64
import json
import re

class CommonJsonResponse:
    """
    Standardized API Response Handler
    """
    
    @staticmethod
    def common_response(
                        status: str,
                        message: str = "",
                        data: Optional[Union[Dict, list, Any]] = None,
                        error: Optional[Dict] = None,
                        pagination: Optional[Dict] = None,
                        status_code: int = HTTPStatus.OK,
                        meta_data: Optional[Dict] = None
                    ):
        
        try:
            response = {
                "status": status.lower(),
                "message": message,
                "meta": {
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "request_id": str(uuid.uuid4()),
                    "status_code": status
                }
            }

            if data is not None:
                response["data"] = data

            if data is not None:
                response["data"] = data

            if error is not None:
                response["error"] = error
                response["meta"].update(meta_data)

            return jsonify(response), status_code

        except Exception as e:


            if data is not None:
                response["data"] = data
            if data is not None:
                response["data"] = data
            error_response = {
                "status": "error",
                "message": "Internal server error while formatting response",
                "meta": {
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "request_id": str(uuid.uuid4()),
                    "error_details": str(e)
                }
            }
            return jsonify(error_response), HTTPStatus.INTERNAL_SERVER_ERROR




class PasswordGenerator:

    def generate_secure_password(self):
        letters = string.ascii_letters
        digits = string.digits
        special_chars = "!@#$%^&*"
        
        password = [
            secrets.choice(letters.upper()),  
            secrets.choice(letters.lower()),   
            secrets.choice(digits),             
            secrets.choice(special_chars),      
        ]
        
        all_characters = letters + digits + special_chars
        password.extend(secrets.choice(all_characters) for _ in range(8)) 
        
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    
from flask_mail import Message
from retail_app.extensions import mail

class EmailService:

    def send_email(subject, recipients, body, html=None):

        print("hhhhh",recipients)
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html
        )
        mail.send(msg)
        return True


class EncryptDecryptService:

    def __init__(self):
        self.key = bytes.fromhex(Config.ENCRYPT_KEY)
        self.nounce = bytes.fromhex(Config.ENCRYPT_NONCE)

    def encrypt_aes_gcm(self,plaintext):
        plaintext = json.dumps(plaintext).encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.nounce)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        encrypt_data = base64.b64encode(ciphertext).decode('utf-8')
        encrypt_tag = base64.b64encode(tag).decode('utf-8')
        resp ={"data": encrypt_data, "tag": encrypt_tag}
        return resp

        
    def decrypt_aes_gcm(self, encrypted_data: str, tag: str):
        try:
            print("encrypted_data", encrypted_data, tag)
            ciphertext = base64.b64decode(encrypted_data)
            tag = base64.b64decode(tag)
            
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.nounce)
            print("cipher",cipher)
            decrypted_text = cipher.decrypt_and_verify(ciphertext, tag)
            print("decrypted_text", decrypted_text)

            resp = decrypted_text.decode('utf-8')
            print("type",type(resp))
            return resp
            
        except ValueError:
            return jsonify({"error": "Decryption failed! Invalid key, nonce, or tampered data."}), 400


class validationService:
    def validate_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def validate_phone(self, phone):
        phone_pattern = r'^\d{10}$'
        return re.match(phone_pattern, phone) is not None


    