from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from app.db import get_database
from app.models import UserModel, OTPModel
from app.schemas import (
    UserRegistrationRequest,
    OTPVerificationRequest,
    LoginRequest,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
)
from app.core import hash_password, verify_password, create_access_token
from app.utils import generate_otp, get_otp_expiration, is_otp_expired, send_otp_sms
from app.core.config import settings


class AuthService:
    """Service layer for authentication operations."""
    
    def __init__(self):
        self.db = None
    
    async def _get_db(self):
        """Get database instance."""
        if self.db is None:
            self.db = get_database()
        return self.db
    
    async def register_user(self, user_data: UserRegistrationRequest) -> dict:
        """
        Register a new user and send OTP for verification.
        
        Args:
            user_data: User registration data
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If phone or email already exists
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Check if phone already exists
        existing_user = await users_collection.find_one({"phone": user_data.phone})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Check if email already exists (if provided)
        if user_data.email:
            existing_email = await users_collection.find_one({"email": user_data.email})
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create user document
        user_dict = {
            "name": user_data.name,
            "surname": user_data.surname,
            "phone": user_data.phone,
            "email": user_data.email,
            "password": hash_password(user_data.password),
            "role": "particulier",
            "is_verified": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None,
            "devices": []
        }
        
        # Insert user
        result = await users_collection.insert_one(user_dict)
        
        # Generate and send OTP
        await self._create_and_send_otp(user_data.phone, "registration")
        
        return {
            "message": "Registration successful",
            "detail": f"A verification code has been sent to {user_data.phone}"
        }
    
    async def verify_otp(self, verification_data: OTPVerificationRequest) -> dict:
        """
        Verify OTP code and activate user account.
        
        Args:
            verification_data: OTP verification data
            
        Returns:
            Authentication response with token
            
        Raises:
            HTTPException: If OTP is invalid or expired
        """
        db = await self._get_db()
        users_collection = db["users"]
        otps_collection = db["otps"]
        
        # Find valid OTP
        otp_record = await otps_collection.find_one({
            "phone": verification_data.phone,
            "is_used": False
        })
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No pending verification found"
            )
        
        # Check if expired
        if is_otp_expired(otp_record["expires_at"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired. Please request a new one"
            )
        
        # Check max attempts
        if otp_record["attempts"] >= settings.OTP_MAX_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum verification attempts exceeded. Please request a new OTP"
            )
        
        # Verify code (compare hashed)
        if not verify_password(verification_data.code, otp_record["code"]):
            # Increment attempts
            await otps_collection.update_one(
                {"_id": otp_record["_id"]},
                {"$inc": {"attempts": 1}}
            )
            
            remaining = settings.OTP_MAX_ATTEMPTS - (otp_record["attempts"] + 1)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid OTP code. {remaining} attempts remaining"
            )
        
        # Mark OTP as used
        await otps_collection.update_one(
            {"_id": otp_record["_id"]},
            {"$set": {"is_used": True}}
        )
        
        # Update user as verified
        user = await users_collection.find_one_and_update(
            {"phone": verification_data.phone},
            {
                "$set": {
                    "is_verified": True,
                    "last_login": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate access token
        access_token = create_access_token(data={"sub": user["phone"], "role": user["role"]})
        
        # Prepare user response
        user["_id"] = str(user["_id"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    async def login(self, login_data: LoginRequest) -> dict:
        """
        Login user with password or OTP.
        
        Args:
            login_data: Login credentials
            
        Returns:
            Authentication response with token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Find user
        user = await users_collection.find_one({"phone": login_data.phone})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if user is verified
        if not user["is_verified"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account not verified. Please verify your phone number"
            )
        
        if login_data.use_otp:
            # Send OTP for login
            await self._create_and_send_otp(login_data.phone, "login")
            return {
                "message": "OTP sent",
                "detail": f"A login code has been sent to {login_data.phone}"
            }
        else:
            # Password login
            if not login_data.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password is required for password login"
                )
            
            if not verify_password(login_data.password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Update last login
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            user["last_login"] = datetime.utcnow()
            
            # Generate access token
            access_token = create_access_token(data={"sub": user["phone"], "role": user["role"]})
            
            # Prepare user response
            user["_id"] = str(user["_id"])
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user
            }
    
    async def request_password_reset(self, reset_data: PasswordResetRequest) -> dict:
        """
        Send OTP for password reset.
        
        Args:
            reset_data: Password reset request data
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If user not found
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Check if user exists
        user = await users_collection.find_one({"phone": reset_data.phone})
        if not user:
            # Don't reveal if user exists or not
            return {
                "message": "If this phone number is registered, you will receive a reset code",
                "detail": None
            }
        
        # Generate and send OTP
        await self._create_and_send_otp(reset_data.phone, "password_reset")
        
        return {
            "message": "Password reset code sent",
            "detail": f"A reset code has been sent to {reset_data.phone}"
        }
    
    async def confirm_password_reset(self, confirm_data: PasswordResetConfirmRequest) -> dict:
        """
        Confirm password reset with OTP and set new password.
        
        Args:
            confirm_data: Password reset confirmation data
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If OTP is invalid
        """
        db = await self._get_db()
        users_collection = db["users"]
        otps_collection = db["otps"]
        
        # Find valid OTP for password reset
        otp_record = await otps_collection.find_one({
            "phone": confirm_data.phone,
            "purpose": "password_reset",
            "is_used": False
        })
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No pending password reset found"
            )
        
        # Check if expired
        if is_otp_expired(otp_record["expires_at"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset code has expired. Please request a new one"
            )
        
        # Verify code
        if not verify_password(confirm_data.code, otp_record["code"]):
            await otps_collection.update_one(
                {"_id": otp_record["_id"]},
                {"$inc": {"attempts": 1}}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset code"
            )
        
        # Mark OTP as used
        await otps_collection.update_one(
            {"_id": otp_record["_id"]},
            {"$set": {"is_used": True}}
        )
        
        # Update password
        await users_collection.update_one(
            {"phone": confirm_data.phone},
            {
                "$set": {
                    "password": hash_password(confirm_data.new_password),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "message": "Password reset successful",
            "detail": "You can now login with your new password"
        }
    
    async def _create_and_send_otp(self, phone: str, purpose: str) -> None:
        """
        Create OTP record and send via SMS.
        
        Args:
            phone: Phone number
            purpose: OTP purpose (registration, login, password_reset)
        """
        db = await self._get_db()
        otps_collection = db["otps"]
        
        # Invalidate any existing OTPs for this phone and purpose
        await otps_collection.update_many(
            {"phone": phone, "purpose": purpose, "is_used": False},
            {"$set": {"is_used": True}}
        )
        
        # Generate new OTP
        otp_code = generate_otp()
        
        # Create OTP record (store hashed code)
        otp_dict = {
            "phone": phone,
            "code": hash_password(otp_code),  # Hash the OTP code
            "purpose": purpose,
            "attempts": 0,
            "created_at": datetime.utcnow(),
            "expires_at": get_otp_expiration(),
            "is_used": False
        }
        
        await otps_collection.insert_one(otp_dict)
        
        # Send OTP via SMS
        await send_otp_sms(phone, otp_code, purpose)


# Create singleton instance
auth_service = AuthService()
