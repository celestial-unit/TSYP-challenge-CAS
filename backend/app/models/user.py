from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Device(BaseModel):
    """Device model for user's registered devices."""
    device_id: str = Field(..., description="Unique device identifier")
    type: str = Field(..., description="Device type (e.g., 'solar_panel', 'inverter', 'battery')")
    registered_at: datetime = Field(default_factory=datetime.utcnow, description="Device registration timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "SP-001-TN-2024",
                "type": "solar_panel",
                "registered_at": "2024-01-15T10:30:00Z"
            }
        }


class UserModel(BaseModel):
    """
    User model for MongoDB storage.
    Represents a user in the SREMS-TN system with role-based fields.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=2, max_length=100, description="User's first name")
    surname: Optional[str] = Field(None, min_length=2, max_length=100, description="User's last name (optional for farmers)")
    phone: str = Field(..., description="User's phone number (unique identifier)")
    email: Optional[str] = Field(None, description="User's email address")
    password: Optional[str] = Field(None, description="Hashed password (optional for OTP-only farmers)")
    role: str = Field(..., description="User role (particulier, agriculteur, technician, operator)")
    is_verified: bool = Field(default=False, description="Whether phone/email is verified")
    profile_completed: bool = Field(default=False, description="Whether profile is fully completed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    devices: List[Device] = Field(default_factory=list, description="List of registered devices")
    
    # Particulier-specific fields
    system_capacity_kwp: Optional[float] = Field(None, description="PV system capacity in kWp")
    has_battery: Optional[bool] = Field(None, description="Battery storage installed")
    address: Optional[str] = Field(None, description="Address or city")
    
    # Agriculteur-specific fields
    farm_location: Optional[str] = Field(None, description="Farm location or GPS coordinates")
    farm_type: Optional[str] = Field(None, description="Type of crops")
    pump_power_kw: Optional[float] = Field(None, description="Pump power in kW")
    water_tank_size: Optional[float] = Field(None, description="Water tank capacity")
    soil_type: Optional[str] = Field(None, description="Soil type")
    irrigation_method: Optional[str] = Field(None, description="Irrigation method (drip/sprinkler)")
    
    # Technician-specific fields
    company_name: Optional[str] = Field(None, description="Maintenance company name")
    certifications: List[str] = Field(default_factory=list, description="Certifications and training")
    
    # Operator-specific fields
    department: Optional[str] = Field(None, description="Department or service")
    access_level: Optional[str] = Field(None, description="Access level (read-only/full)")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Ahmed",
                "surname": "Ben Salem",
                "phone": "+216 98 765 432",
                "email": "ahmed.bensalem@example.tn",
                "role": "particulier",
                "is_verified": True,
                "profile_completed": True,
                "devices": [
                    {
                        "device_id": "SP-001-TN-2024",
                        "type": "solar_panel",
                        "registered_at": "2024-01-15T10:30:00Z"
                    }
                ]
            }
        }


class OTPModel(BaseModel):
    """
    OTP model for MongoDB storage.
    Stores one-time passwords for verification.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    phone: str = Field(..., description="Phone number associated with OTP")
    code: str = Field(..., description="OTP code (hashed)")
    purpose: str = Field(..., description="OTP purpose (registration, login, password_reset)")
    attempts: int = Field(default=0, description="Number of verification attempts")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="OTP creation timestamp")
    expires_at: datetime = Field(..., description="OTP expiration timestamp")
    is_used: bool = Field(default=False, description="Whether OTP has been used")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
