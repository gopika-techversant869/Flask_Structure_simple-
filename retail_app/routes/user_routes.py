from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from retail_app.schemas.userSchemaService import RegisterSchema
from retail_app.service.uesr_reg_service import UserRegisterServiceImpl
from retail_app.decorators import decrypt_request_data


bp = Blueprint("users", __name__)


@bp.route("/users", methods=["POST"])
# @validate()
@decrypt_request_data(schema =RegisterSchema)
def add_user(decrypted_json: RegisterSchema):
    try:
        print("req_daat",decrypted_json)
    except Exception as e:
        print("error", e)
    user = UserRegisterServiceImpl()
    return user.register_user(decrypted_json)
