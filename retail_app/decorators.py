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

def decrypt_request_data(schema=None):  # <-- Accept schema as argument
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

                # Decrypt Data
                enc_obj = EncryptDecryptService()
                decrypted_data = enc_obj.decrypt_aes_gcm(ciphertext, tag)

                if isinstance(decrypted_data, str):  
                    decoded_data = json.loads(decrypted_data)  
                else:
                    decoded_data = decrypted_data  

                # ✅ If a schema is provided, validate the data
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
