from .auth import (
    UserRegistrationRequest,
    OTPVerificationRequest,
    LoginRequest,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
    UserResponse,
    AuthResponse,
    MessageResponse,
    ErrorResponse,
    DeviceSchema,
)

from .role_auth import (
    FarmerRegistrationRequest,
    FarmerProfileCompletionRequest,
    StandardUserRegistrationRequest,
    FarmerLoginRequest,
    StandardLoginRequest,
    ParticulierProfileCompletionRequest,
    TechnicianProfileCompletionRequest,
    OperatorProfileCompletionRequest,
)

__all__ = [
    # Original auth schemas
    "UserRegistrationRequest",
    "OTPVerificationRequest",
    "LoginRequest",
    "PasswordResetRequest",
    "PasswordResetConfirmRequest",
    "UserResponse",
    "AuthResponse",
    "MessageResponse",
    "ErrorResponse",
    "DeviceSchema",
    # Role-based auth schemas
    "FarmerRegistrationRequest",
    "FarmerProfileCompletionRequest",
    "StandardUserRegistrationRequest",
    "FarmerLoginRequest",
    "StandardLoginRequest",
    "ParticulierProfileCompletionRequest",
    "TechnicianProfileCompletionRequest",
    "OperatorProfileCompletionRequest",
]
