from pydantic import BaseModel


# Schema for user registration input
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


# Schema for JWT token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Schema for public user info
class UserOut(BaseModel):
    username: str
    role: str
