# API Endpoint Examples & Payloads - SREMS-TN

Complete request/response examples for all authentication endpoints.

---

## Base URL

```
http://localhost:8000
```

All authentication endpoints are under:
```
http://localhost:8000/api/v1/auth
```

---

## 1. POST /api/v1/auth/register

**Description:** Register a new user (Particulier) and send OTP for verification.

### Request

```http
POST /api/v1/auth/register HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "name": "Ahmed",
  "surname": "Ben Salem",
  "phone": "+216 98 765 432",
  "email": "ahmed.bensalem@example.tn",
  "password": "SecurePass123"
}
```

### Success Response (201 Created)

```json
{
  "message": "Registration successful",
  "detail": "A verification code has been sent to +216 98 765 432"
}
```

### Error Responses

**Phone Already Registered (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Phone number already registered"
}
```

**Email Already Registered (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Email already registered"
}
```

**Invalid Phone Format (422 Unprocessable Entity)**
```json
{
  "detail": [
    {
      "loc": ["body", "phone"],
      "msg": "Invalid phone number format. Use format: +216 98 765 432 or 98 765 432",
      "type": "value_error"
    }
  ]
}
```

**Weak Password (422 Unprocessable Entity)**
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

### CURL Example

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ahmed",
    "surname": "Ben Salem",
    "phone": "+216 98 765 432",
    "email": "ahmed.bensalem@example.tn",
    "password": "SecurePass123"
  }'
```

---

## 2. POST /api/v1/auth/verify

**Description:** Verify phone number with OTP code received via SMS.

### Request

```http
POST /api/v1/auth/verify HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "code": "123456"
}
```

### Success Response (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIrMjE2IDk4IDc2NSA0MzIiLCJyb2xlIjoicGFydGljdWxpZXIiLCJleHAiOjE3Mzc0NTY3ODksImlhdCI6MTczNzM3MDM4OX0.abc123...",
  "token_type": "bearer",
  "user": {
    "_id": "65a1b2c3d4e5f6a7b8c9d0e1",
    "name": "Ahmed",
    "surname": "Ben Salem",
    "phone": "+216 98 765 432",
    "email": "ahmed.bensalem@example.tn",
    "role": "particulier",
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00.000Z",
    "last_login": "2024-01-15T10:35:00.000Z",
    "devices": []
  }
}
```

### Error Responses

**Invalid OTP Code (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Invalid OTP code. 2 attempts remaining"
}
```

**Expired OTP (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "OTP has expired. Please request a new one"
}
```

**Max Attempts Exceeded (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Maximum verification attempts exceeded. Please request a new OTP"
}
```

**No Pending Verification (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "No pending verification found"
}
```

### CURL Example

```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+216 98 765 432",
    "code": "123456"
  }'
```

---

## 3. POST /api/v1/auth/login

**Description:** Login with password or request OTP for login.

### Request (Password Login)

```http
POST /api/v1/auth/login HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "password": "SecurePass123",
  "use_otp": false
}
```

### Success Response - Password Login (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIrMjE2IDk4IDc2NSA0MzIiLCJyb2xlIjoicGFydGljdWxpZXIiLCJleHAiOjE3Mzc0NTY3ODksImlhdCI6MTczNzM3MDM4OX0.abc123...",
  "token_type": "bearer",
  "user": {
    "_id": "65a1b2c3d4e5f6a7b8c9d0e1",
    "name": "Ahmed",
    "surname": "Ben Salem",
    "phone": "+216 98 765 432",
    "email": "ahmed.bensalem@example.tn",
    "role": "particulier",
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00.000Z",
    "last_login": "2024-01-20T14:25:00.000Z",
    "devices": [
      {
        "device_id": "SP-001-TN-2024",
        "type": "solar_panel"
      }
    ]
  }
}
```

### Request (OTP Login)

```http
POST /api/v1/auth/login HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "use_otp": true
}
```

### Success Response - OTP Login (200 OK)

```json
{
  "message": "OTP sent",
  "detail": "A login code has been sent to +216 98 765 432"
}
```

**Note:** After receiving the OTP, use the `/verify` endpoint to complete login.

### Error Responses

**Invalid Credentials (401 Unauthorized)**
```json
{
  "error": "Unauthorized",
  "detail": "Invalid credentials"
}
```

**Account Not Verified (403 Forbidden)**
```json
{
  "error": "Forbidden",
  "detail": "Account not verified. Please verify your phone number"
}
```

**Missing Password (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Password is required for password login"
}
```

### CURL Examples

**Password Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+216 98 765 432",
    "password": "SecurePass123",
    "use_otp": false
  }'
```

**OTP Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+216 98 765 432",
    "use_otp": true
  }'
```

---

## 4. POST /api/v1/auth/reset-password

**Description:** Request password reset by sending OTP to phone number.

### Request

```http
POST /api/v1/auth/reset-password HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "phone": "+216 98 765 432"
}
```

### Success Response (200 OK)

```json
{
  "message": "Password reset code sent",
  "detail": "A reset code has been sent to +216 98 765 432"
}
```

**Note:** For security, this endpoint always returns success even if the phone number doesn't exist.

### CURL Example

```bash
curl -X POST "http://localhost:8000/api/v1/auth/reset-password" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+216 98 765 432"
  }'
```

---

## 5. POST /api/v1/auth/confirm-reset

**Description:** Confirm password reset with OTP and set new password.

### Request

```http
POST /api/v1/auth/confirm-reset HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "phone": "+216 98 765 432",
  "code": "123456",
  "new_password": "NewSecurePass123"
}
```

### Success Response (200 OK)

```json
{
  "message": "Password reset successful",
  "detail": "You can now login with your new password"
}
```

### Error Responses

**Invalid Reset Code (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Invalid reset code"
}
```

**Expired Reset Code (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "Reset code has expired. Please request a new one"
}
```

**No Pending Reset (400 Bad Request)**
```json
{
  "error": "Bad Request",
  "detail": "No pending password reset found"
}
```

**Weak Password (422 Unprocessable Entity)**
```json
{
  "detail": [
    {
      "loc": ["body", "new_password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

### CURL Example

```bash
curl -X POST "http://localhost:8000/api/v1/auth/confirm-reset" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+216 98 765 432",
    "code": "123456",
    "new_password": "NewSecurePass123"
  }'
```

---

## Using JWT Tokens

After successful login or verification, you'll receive an `access_token`. Use this token in the `Authorization` header for protected endpoints:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Example Protected Request

```bash
curl -X GET "http://localhost:8000/api/v1/protected-endpoint" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Testing with Postman

Import this collection structure:

1. Create a new Collection: "SREMS-TN Auth"
2. Add environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: (will be set automatically)
3. Create requests for each endpoint above
4. Set up a test script to automatically save the token:

```javascript
// In Login/Verify request Tests tab
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access_token);
}
```

---

## Field Validation Rules

### Phone Number
- Format: `+216 XX XXX XXX` or `XX XXX XXX`
- Must start with 2, 5, or 9 (Tunisia mobile prefixes)
- Examples: 
  - ✅ `+216 98 765 432`
  - ✅ `98765432`
  - ❌ `+1 234 567 890`

### Password
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- Examples:
  - ✅ `SecurePass123`
  - ✅ `MyP@ssw0rd`
  - ❌ `password` (no uppercase, no digit)
  - ❌ `PASSWORD123` (no lowercase)

### OTP Code
- Exactly 6 digits
- Valid for 10 minutes
- Maximum 3 verification attempts

### Name/Surname
- Minimum 2 characters
- Maximum 100 characters

### Email (Optional)
- Must be valid email format
- Example: `user@example.tn`

---

## Response Status Codes Summary

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful operation |
| 201 | Created | User successfully registered |
| 400 | Bad Request | Invalid data, OTP errors |
| 401 | Unauthorized | Invalid credentials |
| 403 | Forbidden | Unverified account |
| 404 | Not Found | User not found |
| 422 | Unprocessable Entity | Validation errors |
| 500 | Internal Server Error | Server error |

---

**Last Updated:** November 20, 2025
