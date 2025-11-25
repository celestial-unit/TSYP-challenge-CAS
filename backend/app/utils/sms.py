from twilio.rest import Client
from app.core.config import settings
from typing import Optional
import httpx


class SMSProvider:
    """Base class for SMS providers."""
    
    async def send_sms(self, to: str, message: str) -> bool:
        """Send SMS message."""
        raise NotImplementedError


class TwilioProvider(SMSProvider):
    """Twilio SMS provider implementation."""
    
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER
    
    async def send_sms(self, to: str, message: str) -> bool:
        """
        Send SMS via Twilio.
        
        Args:
            to: Recipient phone number
            message: SMS message content
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to
            )
            return True
        except Exception as e:
            print(f" Twilio SMS error: {e}")
            return False


class InfobipProvider(SMSProvider):
    """Infobip SMS provider implementation."""
    
    def __init__(self):
        self.api_key = settings.INFOBIP_API_KEY
        self.base_url = settings.INFOBIP_BASE_URL
        self.sender = settings.INFOBIP_SENDER
    
    async def send_sms(self, to: str, message: str) -> bool:
        """
        Send SMS via Infobip.
        
        Args:
            to: Recipient phone number
            message: SMS message content
            
        Returns:
            True if sent successfully, False otherwise
        """
        url = f"{self.base_url}/sms/2/text/advanced"
        headers = {
            "Authorization": f"App {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {
                    "from": self.sender,
                    "destinations": [{"to": to}],
                    "text": message
                }
            ]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                return response.status_code == 200
        except Exception as e:
            print(f" Infobip SMS error: {e}")
            return False


class MockProvider(SMSProvider):
    """Mock SMS provider for development/testing."""
    
    async def send_sms(self, to: str, message: str) -> bool:
        """
        Mock send SMS (prints to console).
        
        Args:
            to: Recipient phone number
            message: SMS message content
            
        Returns:
            Always True
        """
        print(f"\n📱 [MOCK SMS] To: {to}\n   Message: {message}\n")
        return True


def get_sms_provider() -> SMSProvider:
    """
    Get SMS provider based on configuration.
    
    Returns:
        SMS provider instance
    """
    if settings.ENVIRONMENT == "development" or not settings.SMS_PROVIDER:
        return MockProvider()
    
    if settings.SMS_PROVIDER.lower() == "twilio":
        return TwilioProvider()
    elif settings.SMS_PROVIDER.lower() == "infobip":
        return InfobipProvider()
    else:
        return MockProvider()


async def send_otp_sms(phone: str, otp_code: str, purpose: str = "verification") -> bool:
    """
    Send OTP code via SMS.
    
    Args:
        phone: Recipient phone number
        otp_code: OTP code to send
        purpose: Purpose of OTP (for message customization)
        
    Returns:
        True if sent successfully, False otherwise
    """
    messages = {
        "registration": f"Welcome to SREMS-TN! Your verification code is: {otp_code}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes.",
        "login": f"Your SREMS-TN login code is: {otp_code}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes.",
        "password_reset": f"Your SREMS-TN password reset code is: {otp_code}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes.",
        "verification": f"Your SREMS-TN verification code is: {otp_code}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes."
    }
    
    message = messages.get(purpose, messages["verification"])
    provider = get_sms_provider()
    
    return await provider.send_sms(phone, message)
