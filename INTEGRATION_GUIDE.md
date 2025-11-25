# 🎉 SREMS-TN - Complete Full-Stack Integration Guide

## ✅ What's Been Created

### **Backend (FastAPI)**
- ✅ Complete authentication system with JWT
- ✅ MongoDB integration with Motor (async)
- ✅ OTP verification via SMS (Twilio/Infobip/Mock)
- ✅ User management for "Particulier" role
- ✅ RESTful API with OpenAPI documentation

### **Frontend (Next.js)**
- ✅ Complete Sidebar component with collapsible navigation
- ✅ Zustand state management with persistence
- ✅ Full API integration with backend
- ✅ Login page with authentication flow
- ✅ Dashboard layout with responsive design
- ✅ shadcn/ui components with dark mode support

---

## 🚀 Quick Start

### 1. **Start Backend**

```powershell
# Navigate to backend
cd C:\Users\medma\Desktop\cass\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the server
python main.py
```

Backend will be available at: **http://localhost:8000**

### 2. **Start Frontend**

```powershell
# Navigate to frontend (in a new terminal)
cd C:\Users\medma\Desktop\cass\frontend

# Run development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## 📋 Complete Feature List

### **Sidebar Component**

✅ **Collapsible Design**
- Expand: 256px (w-64)
- Collapsed: 64px (w-16)
- Smooth transitions

✅ **User Section**
- Avatar with initials
- Full name + email display
- Role badge (Particulier)
- Tooltips when collapsed

✅ **Navigation Items**
1. **Dashboard** → `/dashboard`
2. **PV Performance** (with submenu)
   - Overview → `/dashboard/pv`
   - Forecast → `/dashboard/pv/forecast`
   - Soiling Index → `/dashboard/pv/soiling`
   - Energy Loss → `/dashboard/pv/losses`
3. **Devices** (with submenu)
   - My Devices → `/dashboard/devices`
   - Register Device → `/dashboard/devices/register`
   - Device Health → `/dashboard/devices/health`
4. **Profile** → `/dashboard/profile`
5. **Notifications** → `/dashboard/notifications`
6. **Settings** → `/dashboard/settings`

✅ **Features**
- Active route highlighting
- Expandable submenus
- Tooltips for collapsed state
- Logout functionality
- Responsive design
- Dark mode support

---

## 🔗 Backend API Integration

### **Endpoints Used**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/auth/login` | POST | User login |
| `/api/v1/auth/register` | POST | User registration |
| `/api/v1/auth/verify` | POST | OTP verification |
| `/api/v1/auth/reset-password` | POST | Request password reset |
| `/api/v1/auth/confirm-reset` | POST | Confirm password reset |

### **Authentication Flow**

```
Login Form (phone + password)
    ↓
authAPI.login() 
    ↓
POST /api/v1/auth/login
    ↓
Backend validates credentials
    ↓
Returns: { access_token, user }
    ↓
Zustand stores auth state
    ↓
Redirect to /dashboard
```

### **User Data Structure**

```typescript
{
  _id: "65a1b2c3d4e5f6a7b8c9d0e1",
  name: "Ahmed",
  surname: "Ben Salem",
  phone: "+216 98 765 432",
  email: "ahmed@example.tn",
  role: "particulier",
  is_verified: true,
  created_at: "2024-01-15T10:30:00Z",
  last_login: "2024-01-20T14:25:00Z",
  devices: [
    {
      device_id: "SP-001-TN-2024",
      type: "solar_panel"
    }
  ]
}
```

---

## 🗂️ Project Structure

```
cass/
├── backend/
│   ├── app/
│   │   ├── core/           # JWT, security, config
│   │   ├── db/             # MongoDB connection
│   │   ├── models/         # User & OTP models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── routers/        # API endpoints
│   │   └── utils/          # OTP & SMS
│   ├── main.py            # FastAPI app
│   ├── .env               # Environment config
│   └── requirements.txt   # Python dependencies
│
└── frontend/
    ├── app/
    │   ├── dashboard/
    │   │   ├── layout.tsx  # Layout with Sidebar
    │   │   └── page.tsx    # Dashboard home
    │   └── login/
    │       └── page.tsx    # Login page
    ├── components/
    │   ├── dashboard/
    │   │   └── Sidebar.tsx # Main sidebar
    │   └── ui/             # shadcn components
    ├── lib/
    │   ├── api/
    │   │   └── auth.ts     # API client
    │   └── store/
    │       └── auth-store.ts # Zustand store
    ├── .env.local          # Frontend config
    └── package.json
```

---

## 🧪 Testing the Integration

### **1. Create a Test User**

**Option A: Via Swagger UI**
1. Go to http://localhost:8000/api/v1/docs
2. Try `POST /api/v1/auth/register`
3. Use this payload:

```json
{
  "name": "Ahmed",
  "surname": "Ben Salem",
  "phone": "+21698765432",
  "email": "ahmed@example.tn",
  "password": "SecurePass123"
}
```

4. Check backend console for OTP code (in development mode)
5. Use `POST /api/v1/auth/verify` with the OTP code

**Option B: Via Frontend Registration Page**
- Create `/app/register/page.tsx` (similar to login)

### **2. Test Login**

1. Go to http://localhost:3000/login
2. Enter:
   - Phone: `+21698765432`
   - Password: `SecurePass123`
3. Click "Sign In"
4. You should be redirected to `/dashboard`

### **3. Test Sidebar**

1. Once logged in, you should see:
   - Your name and email in the user section
   - "Particulier" badge
   - All navigation items
2. Click the collapse button (top right)
   - Sidebar shrinks to icon-only mode
   - Hover over icons to see tooltips
3. Click on "PV Performance"
   - Submenu expands showing 4 items
4. Click on any navigation item
   - Active state highlights the current page
5. Click "Logout"
   - Auth state cleared
   - Redirected to `/login`

---

## 🎨 Customization

### **Change Sidebar Width**

Edit `components/dashboard/Sidebar.tsx`:

```typescript
// Change these values
isCollapsed ? 'w-16' : 'w-64'  // Default
isCollapsed ? 'w-20' : 'w-72'  // Wider
```

### **Add New Navigation Item**

```typescript
const navigationItems: SidebarItem[] = [
  // ... existing items
  {
    name: 'Analytics',
    href: '/dashboard/analytics',
    icon: BarChart,
    badge: 'New',
  },
];
```

### **Change Color Theme**

Edit `app/globals.css` to modify CSS variables for light/dark themes.

---

## 🔐 Environment Variables

### **Backend (.env)**

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=srems_tn

# JWT
JWT_SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# SMS (Development)
SMS_PROVIDER=mock
ENVIRONMENT=development
```

### **Frontend (.env.local)**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 State Management

### **Zustand Store**

The auth store provides:

```typescript
const {
  user,              // User object or null
  token,             // JWT token or null
  isAuthenticated,   // boolean
  setAuth,           // (user, token) => void
  logout,            // () => void
  updateUser,        // (partial) => void
} = useAuthStore();
```

### **Persistence**

- Stored in localStorage: `srems-auth-storage`
- Survives page refreshes
- Cleared on logout

---

## 🐛 Troubleshooting

### **Backend Not Accessible**

```powershell
# Check if backend is running
curl http://localhost:8000/health
```

Expected: `{"status":"healthy",...}`

### **Frontend Can't Connect to Backend**

1. Check `.env.local` has correct API URL
2. Verify backend is running on port 8000
3. Check browser console for CORS errors
4. Restart Next.js dev server after env changes

### **Login Fails**

1. Verify user exists and is verified
2. Check backend console for errors
3. Verify password is correct
4. Check JWT_SECRET_KEY is set in backend .env

### **Sidebar Not Showing**

1. Check if user is authenticated
2. Verify auth store has user data
3. Check browser console for component errors
4. Ensure all shadcn components are installed

---

## 📚 API Documentation

### **Interactive Docs**

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### **Example API Calls**

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+21698765432",
    "password": "SecurePass123",
    "use_otp": false
  }'
```

**Get Protected Resource (with token):**
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🚀 Next Steps

### **Recommended Additions**

1. **Protected Routes**
   - Add middleware to check authentication
   - Redirect unauthenticated users to `/login`

2. **Registration Page**
   - Create `/app/register/page.tsx`
   - Implement OTP verification flow

3. **Profile Page**
   - Show user details
   - Allow editing name, email
   - Change password functionality

4. **Device Management**
   - Create `/app/dashboard/devices/page.tsx`
   - Add device registration form
   - Show device list

5. **PV Performance Pages**
   - Create chart components
   - Integrate with solar data APIs
   - Add real-time updates

6. **Notifications System**
   - Real-time notifications (WebSocket)
   - Push notifications
   - Email alerts

---

## 💡 Tips

### **Development**

- Use `console.log(useAuthStore.getState())` to debug auth state
- Check Network tab in DevTools for API calls
- Use React DevTools to inspect component props

### **Production**

- Set `ENVIRONMENT=production` in backend
- Configure real SMS provider (Twilio/Infobip)
- Use HTTPS for both frontend and backend
- Set secure `JWT_SECRET_KEY`
- Enable rate limiting
- Add proper error tracking (Sentry)

---

## 📞 Support

For issues or questions:
1. Check backend console for errors
2. Check browser console for frontend errors
3. Review API documentation at `/api/v1/docs`
4. Check this integration guide

---

**🎉 Your SREMS-TN full-stack application is now ready!**

The Sidebar component is production-ready, fully integrated with your FastAPI backend, and ready for further development.
