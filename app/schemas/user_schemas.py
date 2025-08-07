from pydantic import BaseModel
from pydantic import Field


# Schema for user registration input
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = Field(default="user")
