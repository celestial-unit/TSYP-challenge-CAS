# 🎯 SREMS-TN - Quick Reference

## Start Backend
```powershell
cd C:\Users\medma\Desktop\cass\backend
.\venv\Scripts\Activate.ps1
python main.py
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/v1/docs
```

## Start Frontend
```powershell
cd C:\Users\medma\Desktop\cass\frontend
npm run dev
# Frontend: http://localhost:3000
```

## Test Login
1. Register user at http://localhost:8000/api/v1/docs
2. Get OTP from backend console
3. Verify OTP
4. Login at http://localhost:3000/login

## Sidebar Features
- ✅ Collapsible (w-64 ↔ w-16)
- ✅ User info with avatar
- ✅ 6 main navigation items
- ✅ 2 expandable submenus (PV Performance, Devices)
- ✅ Active route highlighting
- ✅ Tooltips when collapsed
- ✅ Logout button

## Tech Stack
**Backend:** FastAPI + MongoDB + JWT + Twilio
**Frontend:** Next.js 15 + Zustand + shadcn/ui + Tailwind

## API Integration
```typescript
import { useAuthStore } from '@/lib/store/auth-store';
import { authAPI } from '@/lib/api/auth';

// Login
await authAPI.login({ phone, password });

// Access user
const { user, logout } = useAuthStore();
```

## File Locations
```
Sidebar: frontend/components/dashboard/Sidebar.tsx
Auth Store: frontend/lib/store/auth-store.ts
API Client: frontend/lib/api/auth.ts
Login Page: frontend/app/login/page.tsx
Dashboard: frontend/app/dashboard/page.tsx
```

## Quick Commands
```powershell
# Backend health check
curl http://localhost:8000/health

# Frontend build
cd frontend && npm run build

# Backend API test
curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d '{"phone":"+21698765432","password":"SecurePass123"}'
```

## Troubleshooting
- Backend errors → Check console + MongoDB connection
- Frontend errors → Check browser console + .env.local
- Login fails → Verify user exists and is verified
- Sidebar not showing → Check auth state in browser DevTools

---
**Full docs:** See INTEGRATION_GUIDE.md
