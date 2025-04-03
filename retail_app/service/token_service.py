from datetime import datetime, timedelta
import jwt
import os
from retail_app.commonutil.commonutil_service import CommonJsonResponse
import uuid

# class TokenService:
#     def __init__(self):
#         # Load secrets from environment variables
#         self.jwt_secret = os.getenv('JWT_SECRET_KEY')
#         self.refresh_secret = os.getenv('JWT_REFRESH_SECRET_KEY')
#         self.jwt_expiry = int(os.getenv('JWT_EXPIRY_MINUTES', '15'))  # 15 minutes default
#         self.refresh_expiry = int(os.getenv('REFRESH_TOKEN_EXPIRY_DAYS', '7'))  # 7 days default
        
#     def generate_tokens(self, user_data):
#         """Generate both access and refresh tokens"""
#         try:
#             # Common token payload
#             current_time = datetime.utcnow()
            
#             # Access token payload
#             access_payload = {
#                 'sub': user_data.get('customer_id'),
#                 'email': user_data.get('username'),
#                 'role': user_data.get('role'),
#                 'type': 'access',
#                 'jti': str(uuid.uuid4()),
#                 'iat': current_time,
#                 'exp': current_time + timedelta(minutes=self.jwt_expiry)
#             }
            
#             # Refresh token payload
#             refresh_payload = {
#                 'user_id': user_data.get('customer_id'),
#                 'type': 'refresh',
#                 'jti': str(uuid.uuid4()),
#                 'iat': current_time,
#                 'exp': current_time + timedelta(days=self.refresh_expiry)
#             }
            
#             # Generate tokens
#             access_token = jwt.encode(
#                 access_payload,
#                 self.jwt_secret,
#                 algorithm='HS256'
#             )
            
#             refresh_token = jwt.encode(
#                 refresh_payload,
#                 self.refresh_secret,
#                 algorithm='HS256'
#             )
            
#             return {
#                 'access_token': access_token,
#                 'refresh_token': refresh_token,
#                 'token_type': 'Bearer',
#                 'expires_in': self.jwt_expiry * 60  # Convert to seconds
#             }
            
#         except Exception as e:
#             raise Exception(f"Token generation failed: {str(e)}")

#     def verify_access_token(self, token):
#         """Verify access token"""
#         try:
#             payload = jwt.decode(
#                 token,
#                 self.jwt_secret,
#                 algorithms=['HS256']
#             )
            
#             # Verify token type
#             if payload.get('type') != 'access':
#                 raise jwt.InvalidTokenError('Invalid token type')
                
#             return payload
            
#         except jwt.ExpiredSignatureError:
#             raise jwt.ExpiredSignatureError('Token has expired')
#         except jwt.InvalidTokenError as e:
#             raise jwt.InvalidTokenError(f'Invalid token: {str(e)}')

#     def verify_refresh_token(self, token):
#         """Verify refresh token"""
#         try:
#             payload = jwt.decode(
#                 token,
#                 self.refresh_secret,
#                 algorithms=['HS256']
#             )
            
#             # Verify token type
#             if payload.get('type') != 'refresh':
#                 raise jwt.InvalidTokenError('Invalid token type')
                
#             return payload
            
#         except jwt.ExpiredSignatureError:
#             raise jwt.ExpiredSignatureError('Refresh token has expired')
#         except jwt.InvalidTokenError as e:
#             raise jwt.InvalidTokenError(f'Invalid refresh token: {str(e)}')

# # Modify your UserRegisterServiceImpl class to include login and token refresh
# class UserRegisterServiceImpl:
#     def __init__(self):
#         self.logger = logging.getLogger(__name__)
#         self.token_service = TokenService()
#         self.bcrypt = Bcrypt()

#     # Your existing register_user method remains the same
    
#     def login_user(self, login_data):
#         try:
#             # Find user by email
#             user = DBService.find_one(
#                 UserAuth,
#                 {"username": login_data.get('email')},
#                 is_mongo=False
#             )
            
#             if not user:
#                 return CommonJsonResponse.common_response(
#                     message="Invalid credentials",
#                     status="failure",
#                     status_code=401
#                 )
            
#             # Verify password
#             if not self.bcrypt.check_password_hash(user.password, login_data.get('password')):
#                 # Update login attempts
#                 user.login_attempts += 1
#                 if user.login_attempts >= 3:
#                     user.is_active = False
#                 DBService.update_record(UserAuth, user, is_mongo=False)
                
#                 return CommonJsonResponse.common_response(
#                     message="Invalid credentials",
#                     status="failure",
#                     status_code=401
#                 )
            
#             # Reset login attempts on successful login
#             user.login_attempts = 0
#             DBService.update_record(UserAuth, user, is_mongo=False)
            
#             # Generate tokens
#             tokens = self.token_service.generate_tokens({
#                 'customer_id': user.customer_id,
#                 'username': user.username,
#                 'role': user.role
#             })
            
#             return CommonJsonResponse.common_response(
#                 "SUCCESS",
#                 "Login successful",
#                 data=tokens,
#                 status_code=200
#             )
            
#         except Exception as e:
#             self.logger.error(f"Login error: {str(e)}")
#             return CommonJsonResponse.common_response(
#                 message="Login failed",
#                 status="failure",
#                 status_code=500
#             )

#     def refresh_token(self, refresh_token):
#         try:
#             # Verify refresh token
#             payload = self.token_service.verify_refresh_token(refresh_token)
            
#             # Get user data
#             user = DBService.find_one(
#                 UserAuth,
#                 {"customer_id": payload['user_id']},
#                 is_mongo=False
#             )
            
#             if not user or not user.is_active:
#                 return CommonJsonResponse.common_response(
#                     message="Invalid refresh token",
#                     status="failure",
#                     status_code=401
#                 )
            
#             # Generate new tokens
#             tokens = self.token_service.generate_tokens({
#                 'customer_id': user.customer_id,
#                 'username': user.username,
#                 'role': user.role
#             })
            
#             return CommonJsonResponse.common_response(
#                 "SUCCESS",
#                 "Token refreshed successfully",
#                 data=tokens,
#                 status_code=200
#             )
            
#         except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
#             return CommonJsonResponse.common_response(
#                 message=str(e),
#                 status="failure",
#                 status_code=401
#             )
#         except Exception as e:
#             self.logger.error(f"Token refresh error: {str(e)}")
#             return CommonJsonResponse.common_response(
#                 message="Token refresh failed",
#                 status="failure",
#                 status_code=500
#             )
