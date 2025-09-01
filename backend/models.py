# backend/models.py
from pydantic import BaseModel

# Pydantic model for user
class User(BaseModel):
    id: int
    email: str
    password: str  # in real apps, this should be hashed
    role: str

# Model for login request
class LoginRequest(BaseModel):
    email: str
    password: str
