from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class DeviceSchema(BaseModel):
    """Schema for device information."""
    device_id: str = Field(..., description="Unique device identifier")
    type: str = Field(..., description="Device type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "SP-001-TN-2024",
                "type": "solar_panel"
            }
        }


# ============= Request Schemas =============

class UserRegistrationRequest(BaseModel):
    """Request schema for user registration."""
    name: str = Field(..., min_length=2, max_length=100, description="First name")
    surname: str = Field(..., min_length=2, max_length=100, description="Last name")
    phone: str = Field(..., description="Phone number (will be used as identifier)")
    email: Optional[EmailStr] = Field(None, description="Email address (optional)")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format (Tunisia format)."""
        # Remove spaces and common separators
        phone_clean = re.sub(r'[\s\-\(\)]', '', v)
        
        # Accept international format +216 or local format starting with 2, 5, 9
        if not re.match(r'^(\+216)?[2-9]\d{7}$', phone_clean):
            raise ValueError("Invalid phone number format. Use format: +216 98 765 432 or 98 765 432")
        
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ahmed",
                "surname": "Ben Salem",
                "phone": "+216 98 765 432",
                "email": "ahmed.bensalem@example.tn",
                "password": "SecurePass123"
            }
        }


class OTPVerificationRequest(BaseModel):
    """Request schema for OTP verification."""
    phone: str = Field(..., description="Phone number")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+216 98 765 432",
                "code": "123456"
            }
        }


class LoginRequest(BaseModel):
    """Request schema for user login."""
    phone: str = Field(..., description="Phone number")
    password: Optional[str] = Field(None, description="Password (for password login)")
    use_otp: bool = Field(default=False, description="Use OTP login instead of password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+216 98 765 432",
                "password": "SecurePass123",
                "use_otp": False
            }
        }


class PasswordResetRequest(BaseModel):
    """Request schema for password reset (send OTP)."""
    phone: str = Field(..., description="Phone number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+216 98 765 432"
            }
        }


class PasswordResetConfirmRequest(BaseModel):
    """Request schema for confirming password reset with OTP."""
    phone: str = Field(..., description="Phone number")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")
    new_password: str = Field(..., min_length=8, description="New password")
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+216 98 765 432",
                "code": "123456",
                "new_password": "NewSecurePass123"
            }
        }


# ============= Response Schemas =============

class UserResponse(BaseModel):
    """Response schema for user data."""
    id: str = Field(..., alias="_id", description="User ID")
    name: str
    surname: str
    phone: str
    email: Optional[str] = None
    role: str
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    devices: List[DeviceSchema] = []
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "65a1b2c3d4e5f6a7b8c9d0e1",
                "name": "Ahmed",
                "surname": "Ben Salem",
                "phone": "+216 98 765 432",
                "email": "ahmed.bensalem@example.tn",
                "role": "particulier",
                "is_verified": True,
                "created_at": "2024-01-15T10:30:00Z",
                "last_login": "2024-01-20T14:25:00Z",
                "devices": [
                    {
                        "device_id": "SP-001-TN-2024",
                        "type": "solar_panel"
                    }
                ]
            }
        }


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "_id": "65a1b2c3d4e5f6a7b8c9d0e1",
                    "name": "Ahmed",
                    "surname": "Ben Salem",
                    "phone": "+216 98 765 432",
                    "email": "ahmed.bensalem@example.tn",
                    "role": "particulier",
                    "is_verified": True,
                    "created_at": "2024-01-15T10:30:00Z",
                    "last_login": "2024-01-20T14:25:00Z",
                    "devices": []
                }
            }
        }


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "OTP sent successfully",
                "detail": "A 6-digit code has been sent to your phone"
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid credentials",
                "detail": "Phone number or password is incorrect"
            }
        }
