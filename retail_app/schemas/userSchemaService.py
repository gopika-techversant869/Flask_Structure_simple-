from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class RegisterSchema(BaseModel):
    name: str
    user_email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    role: str


