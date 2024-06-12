from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserOut(BaseModel):
    email: EmailStr
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str
