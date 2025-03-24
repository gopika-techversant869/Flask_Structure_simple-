from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from flask_simple.schemas.userSchemaService import RegisterSchema
from flask_simple.service.uesr_reg_service import UserRegisterServiceImpl

bp = Blueprint("users", __name__)


@bp.route("/users", methods=["POST"])
@validate()
def add_user(body: RegisterSchema):
    user = UserRegisterServiceImpl()
    return user.register_user(request)

