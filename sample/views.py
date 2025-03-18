
from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from schemas import UserCreate, UserResponse
from services.user_service import UserService
from repositories.user_repository import UserRepository

bp = Blueprint("users", __name__)

# Dependency Injection
user_service = UserService(UserRepository())

@bp.route("/users", methods=["POST"])
@validate()
def add_user(body: UserCreate):
    user = user_service.create_user(body)
    return jsonify(UserResponse.from_orm(user).dict()), 201

@bp.route("/users", methods=["GET"])
def list_users():
    users = user_service.get_users()
    return jsonify([UserResponse.from_orm(user).dict() for user in users])

@bp.route("/users/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(UserResponse.from_orm(user).dict())

@bp.route("/users/<int:user_id>", methods=["PUT"])
@validate()
def modify_user(user_id, body: UserCreate):
    user = user_service.update_user(user_id, body)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(UserResponse.from_orm(user).dict())

@bp.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    if user_service.delete_user(user_id):
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404













