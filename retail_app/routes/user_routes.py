from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from retail_app.schemas.userSchemaService import RegisterSchema
from retail_app.service.uesr_reg_service import UserRegisterServiceImpl

bp = Blueprint("users", __name__)


@bp.route("/users", methods=["POST"])
@validate()
def add_user(body: RegisterSchema):
    user = UserRegisterServiceImpl()
    return user.register_user(body)
