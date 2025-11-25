from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


# ============= Farmer Registration (OTP-only) =============

class FarmerRegistrationRequest(BaseModel):
    """Request schema for farmer registration (name + phone only)."""
    name: str = Field(..., min_length=2, max_length=100, description="First name")
    phone: str = Field(..., description="Phone number (will be used for OTP login)")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format (Tunisia format)."""
        phone_clean = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^(\+216)?[2-9]\d{7}$', phone_clean):
            raise ValueError("Invalid phone number format. Use format: +216 98 765 432")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mohamed",
                "phone": "+216 98 765 432"
            }
        }


class FarmerProfileCompletionRequest(BaseModel):
    """Request schema for completing farmer profile after first login."""
    surname: Optional[str] = Field(None, min_length=2, max_length=100, description="Last name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    farm_location: Optional[str] = Field(None, description="Farm location or GPS coordinates")
    farm_type: Optional[str] = Field(None, description="Type of crops (wheat, olives, etc.)")
    pump_power_kw: Optional[float] = Field(None, gt=0, description="Pump power in kW")
    water_tank_size: Optional[float] = Field(None, gt=0, description="Water tank capacity in liters")
    soil_type: Optional[str] = Field(None, description="Soil type (sandy, clay, loam)")
    irrigation_method: Optional[str] = Field(None, description="Irrigation method (drip, sprinkler)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "surname": "Ben Ali",
                "email": "mohamed.benali@example.tn",
                "farm_location": "Sidi Bouzid",
                "farm_type": "Olives",
                "pump_power_kw": 5.5,
                "water_tank_size": 10000,
                "soil_type": "loam",
                "irrigation_method": "drip"
            }
        }


# ============= Standard Registration (Email + Password) =============

class StandardUserRegistrationRequest(BaseModel):
    """Request schema for standard user registration (particulier, technician, operator)."""
    name: str = Field(..., min_length=2, max_length=100, description="First name")
    surname: str = Field(..., min_length=2, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Email address (login credential)")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    phone: str = Field(..., description="Phone number")
    role: str = Field(..., description="User role (particulier, technician, operator)")
    
    # Role-specific optional fields (filled during registration or later)
    # Particulier fields
    system_capacity_kwp: Optional[float] = Field(None, gt=0, description="PV system capacity in kWp")
    has_battery: Optional[bool] = Field(None, description="Battery storage installed")
    address: Optional[str] = Field(None, description="Address or city")
    
    # Technician fields
    company_name: Optional[str] = Field(None, description="Maintenance company name")
    certifications: Optional[List[str]] = Field(default_factory=list, description="Certifications")
    
    # Operator fields
    department: Optional[str] = Field(None, description="Department or service")
    access_level: Optional[str] = Field(None, description="Access level (read-only, full)")
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        """Validate phone number format."""
        phone_clean = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^(\+216)?[2-9]\d{7}$', phone_clean):
            raise ValueError("Invalid phone number format. Use format: +216 98 765 432")
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
    
    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        """Validate role is one of the allowed values."""
        allowed_roles = ["particulier", "technician", "operator"]
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {', '.join(allowed_roles)}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ahmed",
                "surname": "Ben Salem",
                "email": "ahmed.bensalem@example.tn",
                "password": "SecurePass123",
                "phone": "+216 98 765 432",
                "role": "particulier",
                "system_capacity_kwp": 5.0,
                "has_battery": True,
                "address": "Tunis"
            }
        }


# ============= Login Schemas =============

class FarmerLoginRequest(BaseModel):
    """Request schema for farmer OTP login."""
    phone: str = Field(..., description="Phone number")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+216 98 765 432"
            }
        }


class StandardLoginRequest(BaseModel):
    """Request schema for standard email/password login."""
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "ahmed.bensalem@example.tn",
                "password": "SecurePass123"
            }
        }


# ============= Profile Completion Schemas =============

class ParticulierProfileCompletionRequest(BaseModel):
    """Request schema for completing particulier profile."""
    system_capacity_kwp: Optional[float] = Field(None, gt=0, description="PV system capacity in kWp")
    has_battery: Optional[bool] = Field(None, description="Battery storage installed")
    address: Optional[str] = Field(None, description="Address or city")


class TechnicianProfileCompletionRequest(BaseModel):
    """Request schema for completing technician profile."""
    company_name: Optional[str] = Field(None, description="Maintenance company name")
    certifications: Optional[List[str]] = Field(None, description="Certifications and training")


class OperatorProfileCompletionRequest(BaseModel):
    """Request schema for completing operator profile."""
    department: Optional[str] = Field(None, description="Department or service")
    access_level: Optional[str] = Field(None, description="Access level (read-only, full)")
