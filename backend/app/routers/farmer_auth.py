from fastapi import APIRouter, HTTPException, status
from app.schemas import (
    OTPVerificationRequest,
    AuthResponse,
    MessageResponse,
    ErrorResponse,
)
from app.services import auth_service
from pydantic import BaseModel, Field

router = APIRouter(prefix="/role-auth/farmer", tags=["Farmer Authentication"])


class FarmerLoginRequest(BaseModel):
    """Request model for farmer login (OTP-only)."""
    phone: str = Field(..., description="Farmer's phone number")


class FarmerRegistrationRequest(BaseModel):
    """Request model for farmer registration."""
    name: str = Field(..., min_length=2, max_length=100, description="Farmer's name")
    phone: str = Field(..., description="Phone number in Tunisia format")
    farm_location: str = Field(..., description="Farm location")
    farm_type: str = Field(..., description="Type of crops")


@router.post(
    "/login",
    response_model=MessageResponse,
    summary="Request OTP for farmer login",
    description="Send OTP to farmer's phone for login",
    responses={
        200: {
            "description": "OTP sent successfully",
            "model": MessageResponse
        },
        404: {
            "description": "Farmer account not found",
            "model": ErrorResponse
        }
    }
)
async def farmer_login(login_data: FarmerLoginRequest):
    """
    Request OTP for farmer login.
    
    - **phone**: Farmer's phone number
    
    Sends OTP to the phone if farmer account exists.
    """
    # Check if farmer exists
    from app.db.mongodb import get_database
    db = await get_database()
    
    farmer = await db.users.find_one({
        "phone": login_data.phone,
        "role": "agriculteur"
    })
    
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer account not found"
        )
    
    # Generate and send OTP
    from app.services.auth_service import generate_and_send_otp
    await generate_and_send_otp(login_data.phone, "login")
    
    return MessageResponse(
        message="OTP sent",
        detail=f"A login code has been sent to {login_data.phone}"
    )


@router.post(
    "/verify-otp",
    response_model=AuthResponse,
    summary="Verify farmer OTP",
    description="Verify OTP and login farmer",
    responses={
        200: {
            "description": "Login successful",
            "model": AuthResponse
        },
        400: {
            "description": "Invalid OTP",
            "model": ErrorResponse
        }
    }
)
async def farmer_verify_otp(verification_data: OTPVerificationRequest):
    """
    Verify farmer OTP and complete login.
    
    - **phone**: Farmer's phone number
    - **code**: 6-digit OTP code
    
    Returns JWT access token and farmer information.
    """
    # Verify OTP using existing service
    result = await auth_service.verify_otp(verification_data)
    
    # Check if user is actually a farmer
    if result.user.get("role") != "agriculteur":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a farmer account"
        )
    
    # Check if profile is completed
    profile_completed = result.user.get("profile_completed", False)
    result.user["profile_completed"] = profile_completed
    
    return result


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new farmer",
    description="Register a new farmer and send OTP for verification",
    responses={
        201: {
            "description": "Farmer registered successfully, OTP sent",
            "model": MessageResponse
        },
        400: {
            "description": "Phone already exists",
            "model": ErrorResponse
        }
    }
)
async def farmer_register(farmer_data: FarmerRegistrationRequest):
    """
    Register a new farmer.
    
    - **name**: Farmer's name
    - **phone**: Phone number in Tunisia format
    - **farm_location**: Farm location
    - **farm_type**: Type of crops
    
    Creates farmer account and sends OTP for verification.
    """
    from app.schemas import UserRegistrationRequest
    
    # Convert to general user registration with farmer role
    user_data = UserRegistrationRequest(
        name=farmer_data.name,
        surname="",  # Optional for farmers
        phone=farmer_data.phone,
        email=None,  # Optional for farmers
        password=None,  # Farmers use OTP-only
        role="agriculteur"
    )
    
    # Register using existing service
    result = await auth_service.register_user(user_data)
    
    # Update with farmer-specific fields
    from app.db.mongodb import get_database
    db = await get_database()
    
    await db.users.update_one(
        {"phone": farmer_data.phone},
        {
            "$set": {
                "farm_location": farmer_data.farm_location,
                "farm_type": farmer_data.farm_type,
                "role": "agriculteur"
            }
        }
    )
    
    return result