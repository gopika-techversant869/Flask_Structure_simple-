import jwt
import datetime
from flask import jsonify
from db_service.models import User
from db_service.db import db
# from config.config import SECRET_KEY, MAX_LOGIN_ATTEMPTS
from config.config import Config

def generate_tokens(user):
    """Generate Access & Refresh JWT Tokens"""
    access_payload = {
        "sub": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.datetime.now() + datetime.timedelta(seconds=900)
    }
    refresh_payload = {
        "sub": user.id,
        "exp": datetime.datetime.now() + datetime.timedelta(days=1)
    }

    access_token = jwt.encode(access_payload,Config.JWT_SECRET_KEY,algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, Config.SECRET_KEY, algorithm="HS256")
    print("access_token",access_token,"refresh_token",refresh_token)

    return access_token, refresh_token   

def login_user(username, password):
    """Handles User Login with JWT Authentication"""
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.failed_attempts >= MAX_LOGIN_ATTEMPTS:
        return jsonify({"error": "Account locked due to multiple failed attempts"}), 403

    if not user.check_password(password):
        user.failed_attempts += 1
        db.session.commit()
        return jsonify({"error": "Incorrect password"}), 401

    # Reset failed attempts after successful login
    user.failed_attempts = 0
    db.session.commit()

    access_token, refresh_token = generate_tokens(user)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "role": user.role}), 200
