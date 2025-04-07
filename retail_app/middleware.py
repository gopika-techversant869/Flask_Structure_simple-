# retail_app/decorators/encryption_decorator.py
from functools import wraps
from flask import request
import json
from retail_app.commonutil.commonutil_service import EncryptDecryptService

from flask import request, jsonify
import json
from retail_app.commonutil.commonutil_service import EncryptDecryptService
from retail_app.commonutil.jwt_service import JwtServiceImpl


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




def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Missing token"}), 401

        decoded = JwtServiceImpl.decode_token(token)
        if "error" in decoded:
            return jsonify({"error": decoded["error"]}), 401

        request.user_id = decoded["sub"]
        return f(*args, **kwargs)
    return decorated
