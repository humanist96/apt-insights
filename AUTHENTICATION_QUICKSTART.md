# Authentication System - Quick Start Guide

## Quick Setup (5 minutes)

### Automated Setup

```bash
# Run the setup script
./scripts/setup_auth.sh
```

This will:
1. Check PostgreSQL is running
2. Generate JWT secret key
3. Install Python dependencies
4. Run database migration
5. Install Node.js dependencies
6. Configure environment variables

### Manual Setup

If you prefer manual setup:

**Backend:**
```bash
# 1. Generate JWT secret
openssl rand -hex 32

# 2. Add to fastapi-backend/.env
echo "JWT_SECRET_KEY=<generated-key>" >> fastapi-backend/.env
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/apartment_db" >> fastapi-backend/.env

# 3. Install dependencies
cd fastapi-backend
pip install -r requirements.txt

# 4. Run migration
psql -U postgres -d apartment_db -f migrations/001_create_auth_tables.sql

# 5. Start server
uvicorn main:app --reload
```

**Frontend:**
```bash
# 1. Install dependencies
cd nextjs-frontend
npm install

# 2. Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# 3. Start dev server
npm run dev
```

## Quick Test

### Using the Web UI

1. **Register:** http://localhost:3000/register
2. **Login:** http://localhost:3000/login
3. **Profile:** http://localhost:3000/profile

### Using the Test Script

```bash
cd fastapi-backend
python test_auth.py
```

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234","confirm_password":"Test1234","name":"Test"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test1234"}'

# Get profile (replace TOKEN with access_token from login)
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer TOKEN"
```

## Key Features

### Backend
- JWT-based authentication (24h access, 7d refresh)
- Bcrypt password hashing
- Rate limiting (100 req/hr free, 1000 req/hr authenticated)
- PostgreSQL database
- Automatic token refresh

### Frontend
- React Context for auth state
- Automatic token management
- Protected routes
- Login/Register/Profile pages
- Premium tier support

## Common Tasks

### Add Protected Route

```typescript
import ProtectedRoute from '@/components/ProtectedRoute';

export default function MyPage() {
  return (
    <ProtectedRoute>
      <div>Protected content</div>
    </ProtectedRoute>
  );
}
```

### Check Auth Status

```typescript
import { useAuth } from '@/contexts/AuthContext';

const { user, isAuthenticated } = useAuth();

if (isAuthenticated) {
  // User is logged in
}
```

### Require Premium

```typescript
<ProtectedRoute requirePremium>
  <div>Premium content</div>
</ProtectedRoute>
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login | No |
| POST | `/api/v1/auth/refresh` | Refresh token | No |
| GET | `/api/v1/auth/me` | Get profile | Yes |
| PUT | `/api/v1/auth/me` | Update profile | Yes |
| POST | `/api/v1/auth/logout` | Logout | Yes |

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

## Subscription Tiers

- **Free:** 100 API calls/hour
- **Premium:** 1000 API calls/hour
- **Enterprise:** Unlimited

## Troubleshooting

### Cannot connect to database
```bash
# Check PostgreSQL is running
pg_isready

# If not running
brew services start postgresql
# or
sudo systemctl start postgresql
```

### Token expired
- Tokens auto-refresh on 401 responses
- Access token: 24 hours
- Refresh token: 7 days
- After 7 days, login again required

### CORS errors
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Verify backend CORS middleware is configured

### Rate limit exceeded
- Free users: 100 requests/hour
- Authenticated: 1000 requests/hour
- Wait or upgrade to premium

## Files Created

### Backend
```
fastapi-backend/
├── auth/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── jwt.py
│   ├── dependencies.py
│   └── router.py
├── middleware/
│   └── rate_limiter.py
├── migrations/
│   └── 001_create_auth_tables.sql
└── test_auth.py
```

### Frontend
```
nextjs-frontend/
├── app/
│   ├── login/page.tsx
│   ├── register/page.tsx
│   └── profile/page.tsx
├── contexts/
│   └── AuthContext.tsx
└── components/
    ├── AuthNav.tsx
    └── ProtectedRoute.tsx
```

## Next Steps

1. **Payment Integration** - Connect subscription upgrades (see PAYMENT_INTEGRATION.md)
2. **Email Verification** - Add email confirmation
3. **Password Reset** - Implement forgot password
4. **OAuth** - Add Google/GitHub login
5. **2FA** - Two-factor authentication

## Documentation

- Full documentation: [AUTHENTICATION.md](./AUTHENTICATION.md)
- Payment integration: [PAYMENT_INTEGRATION.md](./PAYMENT_INTEGRATION.md)
- API reference: [fastapi-backend/API_ENDPOINTS.md](./fastapi-backend/API_ENDPOINTS.md)

## Support

For issues or questions:
1. Check [AUTHENTICATION.md](./AUTHENTICATION.md) for detailed info
2. Review error logs in console/terminal
3. Test with `python test_auth.py`
4. Check database connection

---

**Status:** Production Ready ✓
**Last Updated:** 2026-02-08
