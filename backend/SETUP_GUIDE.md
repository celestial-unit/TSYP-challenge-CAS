# Development Setup Guide - SREMS-TN Backend

Step-by-step guide to set up and run the SREMS-TN backend locally.

---

## 📋 Development Checklist

### Phase 1: Environment Setup
- [ ] Install Python 3.9 or higher
- [ ] Install MongoDB 4.4 or higher
- [ ] Install Git (optional)
- [ ] Install Postman or similar API testing tool (optional)

### Phase 2: Project Setup
- [ ] Navigate to project directory
- [ ] Create Python virtual environment
- [ ] Activate virtual environment
- [ ] Install Python dependencies
- [ ] Configure environment variables

### Phase 3: Database Setup
- [ ] Start MongoDB server
- [ ] Verify MongoDB connection
- [ ] Database indexes will be auto-created on first run

### Phase 4: SMS Provider Setup (Choose One)
- [ ] Option A: Use Mock Provider (Development - No Setup Required)
- [ ] Option B: Set up Twilio account and credentials
- [ ] Option C: Set up Infobip account and credentials

### Phase 5: Application Launch
- [ ] Run the FastAPI application
- [ ] Verify API is running
- [ ] Access API documentation
- [ ] Test health check endpoint

### Phase 6: Testing
- [ ] Test user registration
- [ ] Test OTP verification
- [ ] Test login (password)
- [ ] Test login (OTP)
- [ ] Test password reset flow

### Phase 7: Development Workflow
- [ ] Set up code editor (VS Code recommended)
- [ ] Install Python extensions
- [ ] Configure linting (pylint, black)
- [ ] Set up debugging configuration

---

## 🔧 Detailed Setup Instructions

### 1. Install Prerequisites

#### Python 3.9+
Download from: https://www.python.org/downloads/

Verify installation:
```powershell
python --version
```

#### MongoDB
**Option A: Local Installation**
Download from: https://www.mongodb.com/try/download/community

**Option B: MongoDB Atlas (Cloud)**
Sign up at: https://www.mongodb.com/cloud/atlas

**Option C: Docker**
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

Verify MongoDB is running:
```powershell
# If installed locally
mongosh

# If using Docker
docker ps
```

---

### 2. Project Setup

#### Navigate to Project
```powershell
cd c:\Users\medma\Desktop\cass
```

#### Create Virtual Environment
```powershell
python -m venv venv
```

#### Activate Virtual Environment
**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.\venv\Scripts\activate.bat
```

**Git Bash / WSL:**
```bash
source venv/Scripts/activate
```

#### Install Dependencies
```powershell
pip install -r requirements.txt
```

#### Verify Installation
```powershell
pip list
```

Expected packages:
- fastapi
- uvicorn
- motor
- pymongo
- pydantic
- python-jose
- passlib
- twilio (optional)
- etc.

---

### 3. Configure Environment Variables

#### Create .env File
```powershell
Copy-Item .env.example .env
```

#### Edit .env File
Open `.env` in your text editor and configure:

**Required Settings:**
```env
# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=srems_tn

# JWT Secret (Generate a secure random key)
JWT_SECRET_KEY=<generate-a-secure-random-key-here>
```

**Generate JWT Secret:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**SMS Provider (Development):**
```env
# Use mock provider (prints to console)
SMS_PROVIDER=mock
ENVIRONMENT=development
```

**SMS Provider (Production - Twilio):**
```env
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
ENVIRONMENT=production
```

**SMS Provider (Production - Infobip):**
```env
SMS_PROVIDER=infobip
INFOBIP_API_KEY=your_api_key_here
INFOBIP_BASE_URL=https://api.infobip.com
INFOBIP_SENDER=SREMS-TN
ENVIRONMENT=production
```

---

### 4. Database Setup

#### Start MongoDB

**Local MongoDB:**
```powershell
# Windows (if MongoDB is installed as a service)
net start MongoDB

# Manual start
mongod --dbpath C:\data\db
```

**Docker:**
```powershell
docker start mongodb
```

**MongoDB Atlas:**
- Copy your connection string from Atlas dashboard
- Update `MONGODB_URI` in `.env` with your Atlas connection string

#### Verify Connection
```powershell
# Connect to MongoDB
mongosh

# Show databases
show dbs

# Exit
exit
```

---

### 5. Run the Application

#### Start the Server
```powershell
python main.py
```

Or with uvicorn directly:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Verify Server is Running

You should see output like:
```
🚀 Starting SREMS-TN Backend...
✅ Connected to MongoDB: srems_tn
✅ Database indexes created
✅ Application ready on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### 6. Access the Application

#### API Documentation (Swagger UI)
Open in browser: http://localhost:8000/api/v1/docs

#### Alternative Documentation (ReDoc)
Open in browser: http://localhost:8000/api/v1/redoc

#### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "SREMS-TN",
  "version": "1.0.0"
}
```

#### Root Endpoint
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "name": "SREMS-TN",
  "version": "1.0.0",
  "status": "operational",
  "environment": "development",
  "api_docs": "/api/v1/docs"
}
```

---

### 7. Test the API

#### Using Swagger UI (Recommended for Development)
1. Go to http://localhost:8000/api/v1/docs
2. Click on an endpoint (e.g., `POST /api/v1/auth/register`)
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. View the response

#### Using CURL

**Register a User:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ahmed",
    "surname": "Ben Salem",
    "phone": "+216 98 765 432",
    "email": "ahmed@example.tn",
    "password": "SecurePass123"
  }'
```

**Check Console for OTP:**
In development mode, the OTP will be printed to the console:
```
📱 [MOCK SMS] To: +216 98 765 432
   Message: Welcome to SREMS-TN! Your verification code is: 123456. Valid for 10 minutes.
```

**Verify OTP:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+216 98 765 432",
    "code": "123456"
  }'
```

#### Using Postman
1. Import the endpoints from Swagger/OpenAPI spec
2. Create requests for each endpoint
3. Use environment variables for `base_url` and `access_token`

---

### 8. Database Inspection

#### Using MongoDB Compass (GUI)
Download: https://www.mongodb.com/products/compass

Connection string: `mongodb://localhost:27017`

#### Using MongoDB Shell
```bash
mongosh

use srems_tn

# View users
db.users.find().pretty()

# View OTPs
db.otps.find().pretty()

# View indexes
db.users.getIndexes()
db.otps.getIndexes()
```

---

### 9. Development Workflow

#### Code Organization
```
app/
├── core/          # Configuration, JWT, Security
├── db/            # Database connection
├── models/        # MongoDB document models
├── schemas/       # Pydantic validation schemas
├── services/      # Business logic
├── routers/       # API endpoints
└── utils/         # Helper functions
```

#### Making Changes

1. **Edit Code:**
   - Modify files in the `app/` directory
   - Auto-reload is enabled with `--reload` flag

2. **Test Changes:**
   - Use Swagger UI or CURL to test endpoints
   - Check console for errors/logs

3. **Database Changes:**
   - Models are in `app/models/`
   - Indexes are in `app/db/mongodb.py`

#### Common Development Tasks

**Add a New Endpoint:**
1. Add schema to `app/schemas/auth.py`
2. Add service method to `app/services/auth_service.py`
3. Add route to `app/routers/auth.py`
4. Test in Swagger UI

**Modify User Model:**
1. Update `app/models/user.py`
2. Update schemas in `app/schemas/auth.py`
3. Restart the application

**Change OTP Configuration:**
1. Update values in `.env`
2. Restart the application

---

### 10. Troubleshooting

#### Server Won't Start

**Check Python version:**
```powershell
python --version
```
Should be 3.9 or higher.

**Check dependencies:**
```powershell
pip install -r requirements.txt
```

**Check .env file:**
Ensure all required variables are set.

#### Cannot Connect to MongoDB

**Check MongoDB is running:**
```powershell
mongosh
```

**Check connection string in .env:**
```env
MONGODB_URI=mongodb://localhost:27017
```

**Check MongoDB logs:**
```powershell
# Windows
Get-Content "C:\Program Files\MongoDB\Server\6.0\log\mongod.log" -Tail 50
```

#### OTPs Not Working

**In development mode:**
- Check console output for printed OTP codes
- Ensure `ENVIRONMENT=development` in `.env`

**In production mode:**
- Verify SMS provider credentials in `.env`
- Check SMS provider dashboard for delivery status
- Check application logs for SMS errors

#### JWT Token Errors

**Ensure JWT_SECRET_KEY is set:**
```env
JWT_SECRET_KEY=your-secret-key-here
```

**Token expired:**
- Tokens expire after 24 hours by default
- Get a new token by logging in again

#### Import Errors

**Ensure virtual environment is activated:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Reinstall dependencies:**
```powershell
pip install -r requirements.txt --force-reinstall
```

---

### 11. VS Code Setup (Recommended)

#### Install Extensions
- Python (Microsoft)
- Pylance (Microsoft)
- autopep8 or Black Formatter
- MongoDB for VS Code

#### Configure Python Interpreter
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose the virtual environment: `.\venv\Scripts\python.exe`

#### Debug Configuration
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

---

### 12. Next Steps

After setup is complete:

- [ ] Explore the API documentation at `/api/v1/docs`
- [ ] Test all authentication endpoints
- [ ] Review the code structure in `app/`
- [ ] Read `API_EXAMPLES.md` for detailed endpoint examples
- [ ] Consider adding additional user roles (Agriculteur, Technician, etc.)
- [ ] Implement additional features (device management, energy monitoring, etc.)

---

## 🆘 Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Review the `.env` configuration
3. Verify MongoDB is running and accessible
4. Check the API documentation at `/api/v1/docs`
5. Review application logs

---

**Happy Coding! 🚀**
