from fastapi import APIRouter, HTTPException, status
from app.schemas import (
    UserRegistrationRequest,
    OTPVerificationRequest,
    LoginRequest,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
    AuthResponse,
    MessageResponse,
    ErrorResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user (Particulier) and send OTP for phone verification",
    responses={
        201: {
            "description": "User registered successfully, OTP sent",
            "model": MessageResponse
        },
        400: {
            "description": "Phone or email already exists",
            "model": ErrorResponse
        }
    }
)
async def register(user_data: UserRegistrationRequest):
    """
    Register a new user with role 'particulier'.
    
    - **name**: User's first name (2-100 characters)
    - **surname**: User's last name (2-100 characters)
    - **phone**: Phone number in Tunisia format (+216 98 765 432)
    - **email**: Email address (optional)
    - **password**: Password (min 8 chars, must include uppercase, lowercase, and digit)
    
    Returns a success message and sends OTP to the provided phone number.
    """
    return await auth_service.register_user(user_data)


@router.post(
    "/verify",
    response_model=AuthResponse,
    summary="Verify OTP code",
    description="Verify phone number with OTP code and complete registration",
    responses={
        200: {
            "description": "OTP verified successfully, user activated",
            "model": AuthResponse
        },
        400: {
            "description": "Invalid or expired OTP",
            "model": ErrorResponse
        }
    }
)
async def verify_otp(verification_data: OTPVerificationRequest):
    """
    Verify OTP code sent during registration.
    
    - **phone**: Phone number that received the OTP
    - **code**: 6-digit OTP code
    
    Returns JWT access token and user information upon successful verification.
    """
    return await auth_service.verify_otp(verification_data)


@router.post(
    "/login",
    response_model=AuthResponse | MessageResponse,
    summary="Login user",
    description="Login with password or request OTP for login",
    responses={
        200: {
            "description": "Login successful or OTP sent",
        },
        401: {
            "description": "Invalid credentials",
            "model": ErrorResponse
        },
        403: {
            "description": "Account not verified",
            "model": ErrorResponse
        }
    }
)
async def login(login_data: LoginRequest):
    """
    Login user with password or OTP.
    
    - **phone**: User's phone number
    - **password**: User's password (required if use_otp is False)
    - **use_otp**: If True, sends OTP for login instead of password authentication
    
    **Password Login**: Returns JWT access token immediately
    **OTP Login**: Sends OTP to phone, then use /verify endpoint to complete login
    """
    return await auth_service.login(login_data)


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Send OTP for password reset",
    responses={
        200: {
            "description": "Reset code sent",
            "model": MessageResponse
        }
    }
)
async def reset_password(reset_data: PasswordResetRequest):
    """
    Request password reset by sending OTP to phone.
    
    - **phone**: Phone number of the account
    
    Sends a 6-digit reset code to the phone number if account exists.
    """
    return await auth_service.request_password_reset(reset_data)


@router.post(
    "/confirm-reset",
    response_model=MessageResponse,
    summary="Confirm password reset",
    description="Confirm password reset with OTP and set new password",
    responses={
        200: {
            "description": "Password reset successful",
            "model": MessageResponse
        },
        400: {
            "description": "Invalid or expired reset code",
            "model": ErrorResponse
        }
    }
)
async def confirm_password_reset(confirm_data: PasswordResetConfirmRequest):
    """
    Confirm password reset with OTP and set new password.
    
    - **phone**: Phone number of the account
    - **code**: 6-digit reset code received via SMS
    - **new_password**: New password (min 8 chars, must include uppercase, lowercase, and digit)
    
    Resets the password and allows user to login with the new credentials.
    """
    return await auth_service.confirm_password_reset(confirm_data)
