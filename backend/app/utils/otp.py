import random
import string
from datetime import datetime, timedelta
from app.core.config import settings


def generate_otp() -> str:
    """
    Generate a random OTP code.
    
    Returns:
        String of random digits of length OTP_LENGTH
    """
    return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))


def get_otp_expiration() -> datetime:
    """
    Get OTP expiration datetime.
    
    Returns:
        Datetime when OTP should expire
    """
    return datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)


def is_otp_expired(expires_at: datetime) -> bool:
    """
    Check if OTP is expired.
    
    Args:
        expires_at: OTP expiration datetime
        
    Returns:
        True if expired, False otherwise
    """
    return datetime.utcnow() > expires_at
