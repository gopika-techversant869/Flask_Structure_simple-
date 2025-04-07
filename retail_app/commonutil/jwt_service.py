import jwt
from datetime import datetime, timedelta
from retail_app.config.config import Config


class JwtServiceImpl:
    def __init__(self):
        self.JWT_SECRET = Config.JWT_SECRET_KEY
        self.JWT_ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRES_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRES_DAYS = 30

    def generate_jwt_tokens(self, login_id):
        now = datetime.utcnow()

        access_payload = {
            "sub": login_id,
            "type": "access",
            "exp": now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRES_MINUTES),
            "iat": now
        }

        refresh_payload = {
            "sub": login_id,
            "type": "refresh",
            "exp": now + timedelta(days=self.REFRESH_TOKEN_EXPIRES_DAYS),
            "iat": now
        }

        access_token = jwt.encode(access_payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type":"Bearer"
        }

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}

