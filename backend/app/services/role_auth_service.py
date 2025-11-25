from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.db import get_database
from app.models import UserModel
from app.schemas import (
    FarmerRegistrationRequest,
    FarmerProfileCompletionRequest,
    StandardUserRegistrationRequest,
    FarmerLoginRequest,
    StandardLoginRequest,
)
from app.core import hash_password, verify_password, create_access_token
from app.utils import generate_otp, get_otp_expiration, is_otp_expired, send_otp_sms
from app.core.config import settings


class RoleBasedAuthService:
    """Service layer for role-based authentication operations."""
    
    def __init__(self):
        self.db = None
    
    async def _get_db(self):
        """Get database instance."""
        if self.db is None:
            self.db = get_database()
        return self.db
    
    # ============= FARMER AUTHENTICATION (OTP-only) =============
    
    async def register_farmer(self, farmer_data: FarmerRegistrationRequest) -> dict:
        """
        Register a new farmer with only name and phone.
        No password required - will use OTP for login.
        
        Args:
            farmer_data: Farmer registration data (name + phone)
            
        Returns:
            Success message with OTP sent
            
        Raises:
            HTTPException: If phone already exists
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Check if phone already exists
        existing_user = await users_collection.find_one({"phone": farmer_data.phone})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Create farmer document (minimal fields)
        user_dict = {
            "name": farmer_data.name,
            "surname": None,  # Will be completed later
            "phone": farmer_data.phone,
            "email": None,  # Optional, can be added later
            "password": None,  # No password for OTP-only farmers
            "role": "agriculteur",
            "is_verified": False,
            "profile_completed": False,  # Profile incomplete until farm details added
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None,
            "devices": [],
            # Farmer-specific fields (null initially)
            "farm_location": None,
            "farm_type": None,
            "pump_power_kw": None,
            "water_tank_size": None,
            "soil_type": None,
            "irrigation_method": None,
        }
        
        # Insert farmer
        result = await users_collection.insert_one(user_dict)
        
        # Generate and send OTP for verification
        await self._create_and_send_otp(farmer_data.phone, "registration")
        
        return {
            "message": "Farmer registration successful",
            "detail": f"A verification code has been sent to {farmer_data.phone}. Please verify to complete registration."
        }
    
    async def login_farmer_request_otp(self, login_data: FarmerLoginRequest) -> dict:
        """
        Request OTP for farmer login.
        
        Args:
            login_data: Farmer login request (phone only)
            
        Returns:
            Success message with OTP sent
            
        Raises:
            HTTPException: If farmer not found or not verified
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Find farmer
        farmer = await users_collection.find_one({
            "phone": login_data.phone,
            "role": "agriculteur"
        })
        
        if not farmer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farmer account not found"
            )
        
        # Check if farmer is verified
        if not farmer.get("is_verified", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account not verified. Please verify your phone number first."
            )
        
        # Generate and send OTP
        await self._create_and_send_otp(login_data.phone, "login")
        
        return {
            "message": "Login OTP sent",
            "detail": f"A login code has been sent to {login_data.phone}"
        }
    
    async def verify_farmer_otp(self, phone: str, code: str) -> dict:
        """
        Verify OTP for farmer login or registration.
        
        Args:
            phone: Farmer's phone number
            code: OTP code
            
        Returns:
            Authentication response with token
        """
        db = await self._get_db()
        users_collection = db["users"]
        otps_collection = db["otps"]
        
        # Find valid OTP
        otp_record = await otps_collection.find_one({
            "phone": phone,
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
        
        # Verify code
        if not verify_password(code, otp_record["code"]):
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
        
        # Update farmer as verified and set last login
        farmer = await users_collection.find_one_and_update(
            {"phone": phone, "role": "agriculteur"},
            {
                "$set": {
                    "is_verified": True,
                    "last_login": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            },
            return_document=True
        )
        
        if not farmer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farmer account not found"
            )
        
        # Generate access token
        access_token = create_access_token(data={"sub": farmer["phone"], "role": farmer["role"]})
        
        # Prepare user response
        farmer["_id"] = str(farmer["_id"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": farmer,
            "profile_completed": farmer.get("profile_completed", False)
        }
    
    async def complete_farmer_profile(self, phone: str, profile_data: FarmerProfileCompletionRequest) -> dict:
        """
        Complete farmer profile with farm details after first login.
        
        Args:
            phone: Farmer's phone number
            profile_data: Farm and personal details
            
        Returns:
            Updated user data
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Prepare update dictionary
        update_data = {
            "updated_at": datetime.utcnow(),
            "profile_completed": True
        }
        
        # Add provided fields
        if profile_data.surname:
            update_data["surname"] = profile_data.surname
        if profile_data.email:
            update_data["email"] = profile_data.email
        if profile_data.farm_location:
            update_data["farm_location"] = profile_data.farm_location
        if profile_data.farm_type:
            update_data["farm_type"] = profile_data.farm_type
        if profile_data.pump_power_kw is not None:
            update_data["pump_power_kw"] = profile_data.pump_power_kw
        if profile_data.water_tank_size is not None:
            update_data["water_tank_size"] = profile_data.water_tank_size
        if profile_data.soil_type:
            update_data["soil_type"] = profile_data.soil_type
        if profile_data.irrigation_method:
            update_data["irrigation_method"] = profile_data.irrigation_method
        
        # Update farmer profile
        farmer = await users_collection.find_one_and_update(
            {"phone": phone, "role": "agriculteur"},
            {"$set": update_data},
            return_document=True
        )
        
        if not farmer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farmer account not found"
            )
        
        farmer["_id"] = str(farmer["_id"])
        
        return {
            "message": "Profile completed successfully",
            "user": farmer
        }
    
    # ============= STANDARD USER AUTHENTICATION (Email + Password) =============
    
    async def register_standard_user(self, user_data: StandardUserRegistrationRequest) -> dict:
        """
        Register a standard user (particulier, technician, operator) with email/password.
        
        Args:
            user_data: User registration data
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If email or phone already exists
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Check if email already exists
        existing_email = await users_collection.find_one({"email": user_data.email})
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if phone already exists
        existing_phone = await users_collection.find_one({"phone": user_data.phone})
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Create user document
        user_dict = {
            "name": user_data.name,
            "surname": user_data.surname,
            "phone": user_data.phone,
            "email": user_data.email,
            "password": hash_password(user_data.password),
            "role": user_data.role,
            "is_verified": True,  # Email/password users are verified immediately
            "profile_completed": True if user_data.role in ["particulier", "technician", "operator"] else False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_login": None,
            "devices": []
        }
        
        # Add role-specific fields
        if user_data.role == "particulier":
            user_dict.update({
                "system_capacity_kwp": user_data.system_capacity_kwp,
                "has_battery": user_data.has_battery,
                "address": user_data.address
            })
        elif user_data.role == "technician":
            user_dict.update({
                "company_name": user_data.company_name,
                "certifications": user_data.certifications or []
            })
        elif user_data.role == "operator":
            user_dict.update({
                "department": user_data.department,
                "access_level": user_data.access_level or "read-only"
            })
        
        # Insert user
        result = await users_collection.insert_one(user_dict)
        
        return {
            "message": "Registration successful",
            "detail": "You can now login with your email and password"
        }
    
    async def login_standard_user(self, login_data: StandardLoginRequest) -> dict:
        """
        Login standard user with email and password.
        
        Args:
            login_data: Email and password
            
        Returns:
            Authentication response with token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        db = await self._get_db()
        users_collection = db["users"]
        
        # Find user by email
        user = await users_collection.find_one({"email": login_data.email})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify user is not a farmer (farmers use OTP)
        if user.get("role") == "agriculteur":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Farmers must use OTP login. Please use the farmer login page."
            )
        
        # Verify password
        if not user.get("password") or not verify_password(login_data.password, user["password"]):
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
        access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
        
        # Prepare user response
        user["_id"] = str(user["_id"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    
    # ============= SHARED UTILITIES =============
    
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
role_auth_service = RoleBasedAuthService()
