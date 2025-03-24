from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    password: constr(min_length=6)
    role: str


