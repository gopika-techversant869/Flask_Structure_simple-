
 
# import datetime
# import uuid
# from flask import jsonify

# class CommonJsonResponse:

#     def common_response(status="success", message="", data=None, error=None, pagination=None,status_code = None):
#         """
#         Standardized API response format with omitted null values"
#         """
            
#         response = {
#             "status": status,
#             "message": message,
#             "meta": {
#                 "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
#                 "request_id": str(uuid.uuid4())
#             }
#             }

#         if data is not None:
#             response["data"] = data
        
#         if error is not None:
#             response["error"] = error

#         if pagination:
#             response["meta"]["pagination"] = pagination

#         if status_code:
#             response['status_code'] = status_code
        

#         return jsonify(response)

from typing import Optional, Union, Dict, Any, Tuple
from flask import jsonify
from http import HTTPStatus
import datetime
import uuid
import secrets
import string
from flask_mail import Message
from retail_app.extensions import mail

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
            secrets.choice(letters.upper()),    # One uppercase
            secrets.choice(letters.lower()),   
            secrets.choice(digits),             
            secrets.choice(special_chars),      
        ]
        
        # Fill rest of the password
        all_characters = letters + digits + special_chars
        password.extend(secrets.choice(all_characters) for _ in range(8))  # Add 8 more chars
        
        # Shuffle the password characters
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    
from flask_mail import Message
from retail_app.extensions import mail

class EmailService:

    def send_email(subject, recipients, body, html=None):
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html
        )
        mail.send(msg)
        return True


# class EmailService:

#     from retail_app.commonutil import mail

#     def send_mail(self):
#         msg = Message(subject="Hello from Flask!",
#                     recipients=["gopika.na@techversantinfotech.com"],
#                     body="This is a test email sent from a Flask app.")
#         mail.send(msg)
#         return "Email sent!"



from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_aes_gcm(plaintext: bytes, key: bytes, nonce: bytes, aad: bytes = b""):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(aad)

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, encryptor.tag

def decrypt_aes_gcm(ciphertext: bytes, tag: bytes, key: bytes, nonce: bytes, aad: bytes = b""):
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(aad)

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext
