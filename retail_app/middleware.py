# retail_app/decorators/encryption_decorator.py
from functools import wraps
from flask import request
import json
from retail_app.commonutil.commonutil_service import EncryptDecryptService

# def decrypt_request_data():
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             try:
#                 print("req",request)
#                 if request.is_json:

#                     encrypted_data = request.get_json().get('req_data')
#                     print("encrypted_data", encrypted_data)
#                     try:
#                         plaintext = encrypted_data.get('plaintext')
#                         print("plaintext", plaintext)
#                         tag = encrypted_data.get('tag')
#                         print("tag","plain",tag,plaintext)
#                     except Exception as e:
#                         print("error",e)
#                     if encrypted_data:
#                         enc_obj = EncryptDecryptService()
#                         decrypted_data = enc_obj.decrypt_aes_gcm(plaintext, tag)
#                         print("decrypted data",decrypted_data)
#                         request._cached_json = json.loads(decrypted_data)
#                     else:
#                         return {"error": "Encrypted data is required"}, 400
#                 return f(*args, **kwargs)
#             except Exception as e:
#                 return {"error": "Failed to decrypt data"}, 400
#         return decorated_function
#     return decorator

# from flask import request
# import json
# from functools import wraps
# from retail_app.schemas.userSchemaService import RegisterSchema

# def decrypt_request_data():
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             try:
#                 if not request.is_json:
#                     return {"error": "Request must be JSON"}, 400

#                 encrypted_data = request.json.get('req_data')
#                 if not encrypted_data:
#                     return {"error": "Encrypted data is required"}, 400

#                 ciphertext = encrypted_data.get('plaintext')
#                 tag = encrypted_data.get('tag')

#                 if not ciphertext or not tag:
#                     return {"error": "Missing ciphertext or tag"}, 400

#                 # Decrypt Data
#                 enc_obj = EncryptDecryptService()
#                 decrypted_data = enc_obj.decrypt_aes_gcm(ciphertext, tag)

#                 if isinstance(decrypted_data, str):  
#                     decoded_data = json.loads(decrypted_data)  
#                 else:
#                     decoded_data = decrypted_data  

#                 # try:
#                 #     validated_data = RegisterSchema(**decoded_data)  # <-- Ensure it matches schema
#                 #     print("validated_data", validated_data)
#                 # except Exception as e:
#                 #     return {"error": "Invalid decrypted data format", "details": e.errors()}, 400

#                 return f(decoded_data, *args, **kwargs)  # Pass validated data

#             except Exception as e:
#                 print(f"Unexpected error: {str(e)}")
#                 return {"error": "Decryption process failed"}, 500

#         return decorated_function
#     return decorator
from functools import wraps
from flask import request, jsonify
import json
from retail_app.commonutil.commonutil_service import EncryptDecryptService

def decrypt_request_data(schema=None):  
    """
    It decrypts the every request at routes level.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if not request.is_json:
                    return {"error": "Request must be JSON"}, 400

                encrypted_data = request.json.get('req_data')
                if not encrypted_data:
                    return {"error": "Encrypted data is required"}, 400

                ciphertext = encrypted_data.get('plaintext')
                tag = encrypted_data.get('tag')

                if not ciphertext or not tag:
                    return {"error": "Missing ciphertext or tag"}, 400

                enc_obj = EncryptDecryptService()
                decrypted_data = enc_obj.decrypt_aes_gcm(ciphertext, tag)

                if isinstance(decrypted_data, str):  
                    decoded_data = json.loads(decrypted_data)  
                else:
                    decoded_data = decrypted_data  

                if schema:
                    try:
                        validated_data = schema(**decoded_data)  # Dynamically validate
                    except Exception as e:
                        return {"error": "Invalid decrypted data format", "details": str(e)}, 400
                    return f(validated_data, *args, **kwargs)  # Pass validated Pydantic object
                else:
                    return f(decoded_data, *args, **kwargs)  # Pass raw dict if no schema

            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return {"error": "Decryption process failed"}, 500

        return decorated_function
    return decorator


from functools import wraps
from flask import request, jsonify
import jwt
from retail_app. config.config import Config
# from retail_app.db_service.models import User

def verify_token(token):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        user = User.query.get(payload['sub'])
        
        if not user or not user.is_active:
            return None
            
        if user.token_version != payload['token_version']:
            return None
            
        return payload
    except:
        return None

def require_auth(roles=[]):
    """Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Missing or invalid authorization header"}), 401

            token = auth_header.split(' ')[1]
            payload = verify_token(token)

            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401

            if roles and payload['role'] not in roles:
                return jsonify({"error": "Insufficient permissions"}), 403

            request.user = payload
            return f(*args, **kwargs)

        return decorated_function
    return decorator

