from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    full_name: str
    hashed_password: str

class UserInDB(User):
    hashed_password: str
