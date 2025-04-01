from flask import Blueprint, request, jsonify
from retail_app.middleware import require_auth
# from retail_app.db_service.models import User
from retail_app.schemas.userSchemaService import LoginSchema
from retail_app.middleware import decrypt_request_data
from retail_app.service.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@decrypt_request_data(schema = LoginSchema)
def login(decrypted_json:LoginSchema):
    # data = request.get_json()
    # if not data or 'username' not in data or 'password' not in data:
    #     return jsonify({"error": "Username and password required"}), 400
    # return login_user(data['username'], data['password'])
    try:
        print("req_daat",decrypted_json)
    except Exception as e:
        print("error", e)
    user = AuthService()
    return user.login_user(decrypted_json)

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing refresh token"}), 401
    
    token = auth_header.split(' ')[1]
    return refresh_access_token(token)

@auth_bp.route('/logout', methods=['POST'])
@require_auth()
def logout():
    return logout_user(request.user['sub'])

# # Example protected routes
# @auth_bp.route('/profile', methods=['GET'])
# @require_auth(roles=['user', 'admin'])
# def get_profile():
#     user = User.query.get(request.user['sub'])
#     return jsonify({
#         "username": user.username,
#         "email": user.email,
#         "role": user.role
#     })

# @auth_bp.route('/admin/users', methods=['GET'])
# @require_auth(roles=['admin'])
# def get_users():
#     users = User.query.all()
#     return jsonify([{
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "role": user.role,
#         "is_active": user.is_active
#     } for user in users])
