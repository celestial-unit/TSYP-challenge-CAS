# SREMS-TN Backend - Smart Renewable Energy Management System

A professional, modular FastAPI backend for managing renewable energy systems in Tunisia, with a focus on authentication and user management for residential PV owners (Particuliers).

## 🌟 Features

- ✅ **User Registration** with OTP verification via SMS
- ✅ **OTP-based Phone Verification**
- ✅ **Dual Login System** (Password or OTP)
- ✅ **Password Reset** with OTP
- ✅ **Role-based User Management** (starting with "Particulier")
- ✅ **JWT Authentication**
- ✅ **MongoDB Integration** with Motor (async)
- ✅ **API Versioning** (`/api/v1`)
- ✅ **SMS Support** (Twilio, Infobip, or Mock)
- ✅ **Professional Payload Structure**
- ✅ **Comprehensive Error Handling**

## 📁 Project Structure

```
cass/
├── app/
│   ├── __init__.py
│   ├── core/                    # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py           # Settings and configuration
│   │   ├── jwt.py              # JWT token handling
│   │   └── security.py         # Password hashing
│   ├── db/                      # Database
│   │   ├── __init__.py
│   │   └── mongodb.py          # MongoDB connection & indexes
│   ├── models/                  # MongoDB document models
│   │   ├── __init__.py
│   │   └── user.py             # User & OTP models
│   ├── schemas/                 # Pydantic validation schemas
│   │   ├── __init__.py
│   │   └── auth.py             # Request/Response schemas
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   └── auth_service.py     # Authentication service
│   ├── routers/                 # API endpoints
│   │   ├── __init__.py
│   │   └── auth.py             # Auth routes
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── otp.py              # OTP generation
│       └── sms.py              # SMS providers
├── main.py                      # FastAPI application entry
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- MongoDB 4.4+
- SMS Provider account (Twilio/Infobip) or use Mock for development

### Installation

1. **Clone or navigate to the project**
   ```powershell
   cd c:\Users\medma\Desktop\cass
   ```

2. **Create virtual environment**
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```powershell
   Copy-Item .env.example .env
   ```
   
   Edit `.env` and configure:
   - `MONGODB_URI`: Your MongoDB connection string
   - `JWT_SECRET_KEY`: A secure random key
   - SMS provider credentials (Twilio or Infobip)

6. **Run the application**
   ```powershell
   python main.py
   ```
   
   Or with uvicorn:
   ```powershell
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API Documentation: http://localhost:8000/api/v1/docs
   - Alternative Docs: http://localhost:8000/api/v1/redoc
   - Health Check: http://localhost:8000/health

## 📋 API Endpoints

All endpoints are prefixed with `/api/v1`

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user (sends OTP) |
| POST | `/api/v1/auth/verify` | Verify OTP code |
| POST | `/api/v1/auth/login` | Login with password or request OTP |
| POST | `/api/v1/auth/reset-password` | Request password reset (sends OTP) |
| POST | `/api/v1/auth/confirm-reset` | Confirm password reset with OTP |

## 📝 Request/Response Examples

### 1. Register a New User

**Request:**
```json
POST /api/v1/auth/register
Content-Type: application/json

{
  "name": "Ahmed",
  "surname": "Ben Salem",
  "phone": "+216 98 765 432",
  "email": "ahmed.bensalem@example.tn",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "message": "Registration successful",
  "detail": "A verification code has been sent to +216 98 765 432"
}
```

### 2. Verify OTP

**Request:**
```json
POST /api/v1/auth/verify
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "65a1b2c3d4e5f6a7b8c9d0e1",
    "name": "Ahmed",
    "surname": "Ben Salem",
    "phone": "+216 98 765 432",
    "email": "ahmed.bensalem@example.tn",
    "role": "particulier",
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-15T10:35:00Z",
    "devices": []
  }
}
```

### 3. Login (Password)

**Request:**
```json
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "password": "SecurePass123",
  "use_otp": false
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "65a1b2c3d4e5f6a7b8c9d0e1",
    "name": "Ahmed",
    "surname": "Ben Salem",
    "phone": "+216 98 765 432",
    "email": "ahmed.bensalem@example.tn",
    "role": "particulier",
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-20T14:25:00Z",
    "devices": []
  }
}
```

### 4. Login (OTP - Step 1: Request OTP)

**Request:**
```json
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "use_otp": true
}
```

**Response:**
```json
{
  "message": "OTP sent",
  "detail": "A login code has been sent to +216 98 765 432"
}
```

Then use `/verify` endpoint with the OTP code to complete login.

### 5. Reset Password (Step 1: Request OTP)

**Request:**
```json
POST /api/v1/auth/reset-password
Content-Type: application/json

{
  "phone": "+216 98 765 432"
}
```

**Response:**
```json
{
  "message": "Password reset code sent",
  "detail": "A reset code has been sent to +216 98 765 432"
}
```

### 6. Reset Password (Step 2: Confirm with OTP)

**Request:**
```json
POST /api/v1/auth/confirm-reset
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "code": "123456",
  "new_password": "NewSecurePass123"
}
```

**Response:**
```json
{
  "message": "Password reset successful",
  "detail": "You can now login with your new password"
}
```

## 👤 User Data Model (Particulier)

```json
{
  "_id": "ObjectId (auto-generated)",
  "name": "string (2-100 chars)",
  "surname": "string (2-100 chars)",
  "phone": "string (unique, Tunisia format)",
  "email": "string (optional, unique if provided)",
  "password": "string (hashed with bcrypt)",
  "role": "particulier",
  "is_verified": "boolean (default: false)",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)",
  "last_login": "datetime (ISO 8601, nullable)",
  "devices": [
    {
      "device_id": "string",
      "type": "string",
      "registered_at": "datetime (ISO 8601)"
    }
  ]
}
```

## 🔐 Security Features

- **Password Requirements**:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  
- **OTP Security**:
  - 6-digit codes
  - 10-minute expiration
  - Maximum 3 verification attempts
  - Hashed storage in database
  - Auto-deletion via MongoDB TTL index

- **Phone Validation**:
  - Tunisia format: `+216 98 765 432` or `98 765 432`
  - Starts with 2, 5, or 9 (Tunisia mobile prefixes)

## ⚙️ Configuration

Key environment variables (see `.env.example`):

```env
# Database
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=srems_tn

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# OTP
OTP_LENGTH=6
OTP_EXPIRE_MINUTES=10
OTP_MAX_ATTEMPTS=3

# SMS Provider (choose one)
SMS_PROVIDER=twilio  # or infobip, or leave empty for mock
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

## 🧪 Development Mode

In development (`ENVIRONMENT=development`), the app uses a **Mock SMS Provider** that prints OTP codes to the console instead of sending real SMS messages.

Example console output:
```
📱 [MOCK SMS] To: +216 98 765 432
   Message: Welcome to SREMS-TN! Your verification code is: 123456. Valid for 10 minutes.
```

## 🗂️ Database Indexes

Automatically created on startup:

**Users Collection:**
- Unique index on `phone`
- Sparse index on `email`
- Index on `role`
- Index on `created_at`

**OTPs Collection:**
- Compound index on `phone` + `purpose`
- TTL index on `expires_at` (auto-delete expired OTPs)

## 🔄 Future Role Extensions

The architecture is designed to easily support additional user roles:

- **Agriculteur** (Farmers)
- **Technician** (Solar Technicians)
- **Operator** (System Operators)

Simply add new roles and extend the schemas/services as needed.

## 📊 Development Checklist

- [x] Set up Python virtual environment
- [x] Install dependencies
- [x] Configure .env for DB URI, JWT secret, SMS API keys
- [x] Create MongoDB User model and indexes
- [x] Implement OTP generation and expiration logic
- [x] Implement JWT token creation and validation
- [x] Create routers and link to main.py
- [x] Implement error handling and response models
- [x] Write example request/response payloads
- [x] Modularize code for future roles

## 🐛 Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors, invalid data)
- `401` - Unauthorized (invalid credentials)
- `403` - Forbidden (unverified account)
- `404` - Not Found
- `500` - Internal Server Error

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Motor Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Twilio SMS Documentation](https://www.twilio.com/docs/sms)

## 📄 License

This project is part of the Smart Renewable Energy Management System for Tunisia (SREMS-TN).

## 🤝 Contributing

This is a modular, professional architecture ready for team development and future expansion.

---

**Built with ❤️ using FastAPI, MongoDB, and Python**
