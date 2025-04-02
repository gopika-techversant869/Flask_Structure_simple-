from pydantic import BaseModel, EmailStr, constr
from typing import Optional





class LoginSchema(BaseModel):
    username: constr(strip_whitespace=True,min_length=3,max_length=50)
    password: constr(min_length=6, max_length=128)

class RegisterSchema(BaseModel):
    name: str
    user_email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    role: str


