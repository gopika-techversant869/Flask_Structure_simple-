import jwt
import datetime
from datetime import timedelta
import uuid
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash


from flask import jsonify, current_app
# from retail_app.db_service.models import User
from retail_app.db_service.db import db
from retail_app.config.config import Config
from retail_app.db_service.models import Customer
from retail_app.db_service.models import UserAuth
from retail_app.commonutil.commonutil_service import CommonJsonResponse
from retail_app.db_service.db_common_service import DBService
from retail_app.commonutil.commonutil_service import EncryptDecryptService


bcrypt = Bcrypt()


class AuthService:
    def __init__(self):
        self.logger = current_app.logger

    def generate_tokens(self,user_data):
        """Generate both access and refresh tokens"""

        try:
            current_time = datetime.utcnow()
            
            access_payload = {
                'sub': user_data.get('customer_id'),
                'email': user_data.get('username'),
                'role': user_data.get('role'),
                'type': 'access',
                'jti': str(uuid.uuid4()),
                'iat': current_time,
                'exp': current_time + timedelta(minutes = Config.JWT_ACCESS_TOKEN_EXPIRES)
            }
            
            refresh_payload = {
                'user_id': user_data.get('customer_id'),
                'type': 'refresh',
                'jti': str(uuid.uuid4()),
                'iat': current_time,
                'exp': current_time + timedelta(days = Config.REFRESH_TOKEN_EXPIRE_DAYS)
            }
            
            access_token = jwt.encode(access_payload,Config.JWT_SECRET_KEY,algorithm='HS256')
            refresh_token = jwt.encode(refresh_payload,self.refresh_secret,algorithm='HS256')
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': Config.JWT_ACCESS_TOKEN_EXPIRES * 60  
            }
            
        except Exception as e:
            raise Exception(f"Token generation failed: {str(e)}")

    def login_user(self,data):
        """Handle user login with security measures"""

        try:
            user = DBService.find_one(UserAuth,{"username": data.username},is_mongo=False)
            print("user data",user.is_active)
            if not user:
               return CommonJsonResponse.common_response(
                                                        status="FAILURE",
                                                        message="User not found",
                                                        status_code=400
                                                        )
            if not user.is_active:
                return CommonJsonResponse.common_response(
                                                        status = "FAILURE",
                                                        message="User not active",
                                                        status_code=403
                                                        )
            if not bcrypt.check_password_hash(user.password, data.password):
                update_data = {"login_attempts": user.login_attempts + 1}
                
                if user.login_attempts + 1 >= Config.MAX_LOGIN_ATTEMPTS:
                    update_data["is_active"] = False
                
                DBService.update_record(UserAuth, {"id": user.id}, update_data, is_mongo=False)
                return CommonJsonResponse.common_response(
                                                        status = "FAILURE",
                                                        message="Invalid credentials", 
                                                        status_code=401
                                                        )

            DBService.update_record(UserAuth, {"id": user.id}, {"failed_attempts": 0, "last_login": datetime.datetime.utcnow()}, is_mongo=False)

            token = AuthService.generate_tokens(user)
            
            resp_dict = {
                "access_token":token.get('access_token'),
                "refresh_token":token.get('refresh_token'),
                "token_type":token.get('token_type'),
                "expires_in":token.get('expires_in'),
                "role":user.role,
                "username":user.username
            }

            enc_obj = EncryptDecryptService()
            
            encrypt_resp = enc_obj.encrypt_aes_gcm(resp_dict)
            print("encrypt_resp",encrypt_resp)
            return CommonJsonResponse.common_response(status="SUCCESS",message="Login successful", data=encrypt_resp, status_code=200)

        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            return jsonify({"error": "Login failed"}), 500
        

    def refresh_access_token(refresh_token):
        """Generate new access token using refresh token"""

        try:
            payload = jwt.decode(
                refresh_token,
                Config.JWT_REFRESH_SECRET_KEY,
                algorithms=["HS256"]
            )

            if payload['type'] != 'refresh':
                return jsonify({"error": "Invalid token type"}), 401

            user = User.query.get(payload['sub'])
            
            if not user or not user.is_active:
                return jsonify({"error": "User not found or inactive"}), 401

            if user.token_version != payload['token_version']:
                return jsonify({"error": "Token version mismatch"}), 401

            new_access_token = generate_tokens(user)[0]

            return jsonify({
                "access_token": new_access_token,
                "message": "Token refreshed successfully"
            }), 200

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Refresh token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid refresh token"}), 401
        except Exception as e:
            current_app.logger.error(f"Token refresh error: {str(e)}")
            return jsonify({"error": "Token refresh failed"}), 500

    def logout_user(user_id):
        """Handle user logout"""
        try:
            user = User.query.get(user_id)
            if user:
                user.token_version += 1  # Invalidate all existing tokens
                db.session.commit()
                return jsonify({"message": "Logout successful"}), 200
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            current_app.logger.error(f"Logout error: {str(e)}")
            return jsonify({"error": "Logout failed"}), 500
