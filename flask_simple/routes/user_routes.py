from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from flask_simple.service.userService import UserService
from flask_simple.schemas.userSchemaService import UserCreate

bp = Blueprint("users", __name__)

user_service = UserService()

@bp.route("/users", methods=["POST"])
@validate()
def add_user(body: UserCreate):
    user = user_service.create_user(body.name, body.email)
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201

@bp.route("/users", methods=["GET"])
def list_users():
    users = user_service.get_users()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])
