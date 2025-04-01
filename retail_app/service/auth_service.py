import jwt
import datetime
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



bcrypt = Bcrypt()


class AuthService:
    def __init__(self):
        self.logger = current_app.logger

    def generate_tokens(user):
        """Generate both Access and Refresh JWT Tokens"""
        jti = str(uuid.uuid4())
        
        access_payload = {
            "sub": user.id,
            "username": user.username,
            "role": user.role,
            "type": "access",
            "jti": jti,
            "token_version": user.token_version,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.TOKEN_EXPIRE_MINUTES)
        }

        refresh_payload = {
            "sub": user.id,
            "type": "refresh",
            "jti": str(uuid.uuid4()),
            "token_version": user.token_version,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
        }

        access_token = jwt.encode(access_payload, Config.JWT_SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, Config.JWT_REFRESH_SECRET_KEY, algorithm="HS256")

        return access_token, refresh_token
            # Successful login

    def login_user(self,data):
        """Handle user login with security measures"""
        try:
            user = DBService.find_one(UserAuth,{"username": data.username},is_mongo=False)
            print("user data",user.is_active)
            
            if not user:
               return CommonJsonResponse.common_response(status="FAILURE",message="User not found",status_code=400)

            if not user.is_active:
                return CommonJsonResponse.common_response(status = "FAILURE",message="User not active",status_code=403)

            # if user.login_attempts >= Config.MAX_LOGIN_ATTEMPTS:
            #     return CommonJsonResponse.common_response(status="FAILURE",message="Account has been locked!please contact the support",status_code=403)
            # hash_pwd = generate_password_hash(data.password)

            # print("hash_pwd", hash_pwd) 
            # print("pwd",user.password)          
            #     user.login_attempts += 1
            #     if user.login_attempts >= Config.MAX_LOGIN_ATTEMPTS:
            #         user.is_active = False
            #     db.session.commit()
            #     return CommonJsonResponse.common_response(message="Invalid credentials", status_code=401)
            hash_pwd = bcrypt.generate_password_hash(data.password).decode('utf-8')
            print("hasg=h",hash_pwd)
            print("db pass",user.password)


            if hash_pwd != user.password:
                update_data = {"login_attempts": user.login_attempts + 1}

                if user.login_attempts + 1 >= Config.MAX_LOGIN_ATTEMPTS:
                    update_data["is_active"] = False

                DBService.update_record(UserAuth, {"id": user.id}, update_data, is_mongo=False)

                return CommonJsonResponse.common_response(message="Invalid credentials", status_code=401)

            DBService.update_record(UserAuth, {"id": user.id}, {"failed_attempts": 0, "last_login": datetime.datetime.utcnow()}, is_mongo=False)


            access_token, refresh_token = AuthService.generate_tokens(user)

            resp_dict = {
                "access_token":access_token,
                "refresh_token":refresh_token,
                "role":user.role,
                "username":user.username
            }
            return CommonJsonResponse.common_response(status="SUCCESS",message="Login successful", data=resp_dict, status_code=200)

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
