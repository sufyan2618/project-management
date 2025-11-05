from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from typing import Optional
import re

from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(
        max_length=100,
        description="Password must contain uppercase, lowercase, number, and special character"
    )
    full_name: Optional[str] = Field(
        min_length=3,
        max_length=100,
        description="The full name of the user"
    )
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        # Check minimum length
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for uppercase
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Check for lowercase
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for digit
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        
        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)')
        
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    created_at: datetime

