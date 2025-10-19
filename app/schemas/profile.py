from pydantic import BaseModel


class User(BaseModel):
    """
    User model
    """
    email: str
    name: str
    stack: str


class ProfileResponse(BaseModel):
    """
    Profile response model
    """
    status: str
    user: User
    timestamp: str
    fact: str
