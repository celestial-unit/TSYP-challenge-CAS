from fastapi import APIRouter, HTTPException, status, Header
from app.schemas import (
    FarmerRegistrationRequest,
    FarmerProfileCompletionRequest,
    StandardUserRegistrationRequest,
    FarmerLoginRequest,
    StandardLoginRequest,
    OTPVerificationRequest,
    MessageResponse,
    ErrorResponse,
)
from app.services.role_auth_service import role_auth_service

router = APIRouter(prefix="/role-auth", tags=["Role-Based Authentication"])


# ============= FARMER ENDPOINTS =============

@router.post(
    "/farmer/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new farmer",
    description="Register a farmer with only name and phone number. OTP will be sent for verification."
)
async def register_farmer(farmer_data: FarmerRegistrationRequest):
    """
    Register a new farmer (Agriculteur) with minimal information.
    
    - **name**: Farmer's first name
    - **phone**: Phone number (will receive OTP)
    
    Remaining profile fields (farm location, pump details, etc.) can be completed later in dashboard.
    """
    return await role_auth_service.register_farmer(farmer_data)


@router.post(
    "/farmer/login",
    response_model=MessageResponse,
    summary="Request OTP for farmer login",
    description="Send OTP to farmer's phone for login"
)
async def farmer_login_request_otp(login_data: FarmerLoginRequest):
    """
    Request OTP for farmer login.
    
    - **phone**: Farmer's phone number
    
    An OTP will be sent to the phone number for login verification.
    """
    return await role_auth_service.login_farmer_request_otp(login_data)


@router.post(
    "/farmer/verify-otp",
    summary="Verify farmer OTP",
    description="Verify OTP code for farmer login or registration"
)
async def verify_farmer_otp(verification_data: OTPVerificationRequest):
    """
    Verify OTP code for farmer login or registration.
    
    - **phone**: Farmer's phone number
    - **code**: 6-digit OTP code
    
    Returns JWT token and user information upon successful verification.
    """
    return await role_auth_service.verify_farmer_otp(
        verification_data.phone,
        verification_data.code
    )


@router.post(
    "/farmer/complete-profile",
    summary="Complete farmer profile",
    description="Complete farmer profile with farm details after first login"
)
async def complete_farmer_profile(
    profile_data: FarmerProfileCompletionRequest,
    authorization: str = Header(...)
):
    """
    Complete farmer profile with farm and personal details.
    
    This endpoint should be called after the farmer's first login to add:
    - Surname, email (optional)
    - Farm location, type of crops
    - Pump power, water tank size
    - Soil type, irrigation method
    
    Requires authentication (JWT token in Authorization header).
    """
    # TODO: Extract phone from JWT token
    # For now, we'll need to pass phone in the request
    # In production, decode the JWT and get phone from there
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Profile completion endpoint requires JWT authentication middleware"
    )


# ============= STANDARD USER ENDPOINTS =============

@router.post(
    "/standard/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a standard user",
    description="Register a user with email and password (Particulier, Technician, Operator)"
)
async def register_standard_user(user_data: StandardUserRegistrationRequest):
    """
    Register a standard user (Particulier, Technician, or Operator).
    
    - **name**: First name
    - **surname**: Last name
    - **email**: Email address (login credential)
    - **password**: Password (min 8 chars, uppercase, lowercase, digit)
    - **phone**: Phone number
    - **role**: User role (particulier, technician, operator)
    
    Role-specific fields can be provided during registration or completed later:
    - **Particulier**: system_capacity_kwp, has_battery, address
    - **Technician**: company_name, certifications
    - **Operator**: department, access_level
    """
    return await role_auth_service.register_standard_user(user_data)


@router.post(
    "/standard/login",
    summary="Login with email and password",
    description="Login for standard users (Particulier, Technician, Operator)"
)
async def login_standard_user(login_data: StandardLoginRequest):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns JWT access token and user information.
    """
    return await role_auth_service.login_standard_user(login_data)


# ============= PROFILE COMPLETION ENDPOINTS =============
# Note: These should be protected with JWT authentication middleware

@router.get(
    "/user/profile",
    summary="Get current user profile",
    description="Get authenticated user's profile information"
)
async def get_user_profile(authorization: str = Header(...)):
    """
    Get current user's profile.
    
    Requires authentication (JWT token in Authorization header).
    """
    # TODO: Implement JWT authentication middleware
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Profile endpoint requires JWT authentication middleware"
    )
