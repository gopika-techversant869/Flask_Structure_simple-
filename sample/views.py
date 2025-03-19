from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from schemas import UserCreate, OrderCreate
from service.userService import UserService

bp = Blueprint("users", __name__)

# Initialize service
user_service = UserService()

@bp.route("/users", methods=["POST"])
@validate()
def add_user(body: UserCreate):
    """Handles POST request, sends data to service layer."""
    user = user_service.create_user(body)  
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201

@bp.route("/users", methods=["GET"])
def list_users():
    """Handles GET request, asks service layer for users."""
    users = user_service.get_users()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])