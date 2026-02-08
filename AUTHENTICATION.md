# Authentication System Documentation

## Overview

Complete user authentication system for the Korean apartment analysis platform with JWT-based authentication, role-based access control, and subscription tier management.

## Backend (FastAPI)

### Directory Structure

```
fastapi-backend/
├── auth/
│   ├── __init__.py         # Module exports
│   ├── database.py         # Database configuration
│   ├── models.py           # SQLAlchemy models (User, Subscription)
│   ├── schemas.py          # Pydantic schemas
│   ├── jwt.py              # JWT token generation/validation
│   ├── dependencies.py     # FastAPI dependencies
│   └── router.py           # Auth endpoints
├── middleware/
│   └── rate_limiter.py     # Rate limiting middleware
└── migrations/
    └── 001_create_auth_tables.sql  # Database migration
```

### Database Schema

**Users Table:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    subscription_tier subscription_tier DEFAULT 'free',
    subscription_expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);
```

**Subscriptions Table:**
```sql
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    status subscription_status DEFAULT 'active'
);
```

### API Endpoints

#### POST `/api/v1/auth/register`
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### POST `/api/v1/auth/login`
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### POST `/api/v1/auth/refresh`
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### GET `/api/v1/auth/me`
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "subscription_tier": "free",
  "subscription_expires_at": null,
  "created_at": "2026-02-08T10:00:00Z",
  "last_login_at": "2026-02-08T10:00:00Z"
}
```

#### PUT `/api/v1/auth/me`
Update current user profile (requires authentication).

**Request:**
```json
{
  "name": "John Smith",
  "email": "newmail@example.com"
}
```

#### POST `/api/v1/auth/logout`
Logout current user (requires authentication).

### JWT Configuration

- **Access Token Expiry:** 24 hours
- **Refresh Token Expiry:** 7 days
- **Algorithm:** HS256
- **Secret Key:** Set via `JWT_SECRET_KEY` environment variable

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

### Rate Limiting

- **Free tier:** 100 requests/hour
- **Authenticated users:** 1000 requests/hour
- **Premium users:** Unlimited

Headers returned:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1707392400
```

### Security Features

1. **Password Hashing:** Bcrypt with salt rounds
2. **JWT Tokens:** HS256 algorithm with expiration
3. **Token Refresh:** Automatic token rotation
4. **Rate Limiting:** IP-based with per-tier limits
5. **CORS:** Configured for frontend domain
6. **Input Validation:** Pydantic schemas with validators

## Frontend (Next.js)

### Directory Structure

```
nextjs-frontend/
├── app/
│   ├── login/
│   │   └── page.tsx        # Login page
│   ├── register/
│   │   └── page.tsx        # Registration page
│   ├── profile/
│   │   └── page.tsx        # User profile page
│   └── providers.tsx       # App providers (includes AuthProvider)
├── contexts/
│   └── AuthContext.tsx     # Auth context and hooks
└── components/
    ├── AuthNav.tsx         # Auth navigation component
    └── ProtectedRoute.tsx  # Protected route HOC
```

### Auth Context

The `AuthProvider` manages authentication state and provides:

```typescript
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, confirmPassword: string, name?: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}
```

### Usage Examples

#### Using the Auth Hook

```typescript
'use client';

import { useAuth } from '@/contexts/AuthContext';

export default function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();

  if (!isAuthenticated) {
    return <p>Please log in</p>;
  }

  return (
    <div>
      <p>Welcome, {user?.name}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

#### Protected Routes

```typescript
import ProtectedRoute from '@/components/ProtectedRoute';

export default function ProtectedPage() {
  return (
    <ProtectedRoute>
      <div>This content is only visible to authenticated users</div>
    </ProtectedRoute>
  );
}
```

#### Premium-Only Content

```typescript
import ProtectedRoute from '@/components/ProtectedRoute';

export default function PremiumPage() {
  return (
    <ProtectedRoute requirePremium>
      <div>Premium content</div>
    </ProtectedRoute>
  );
}
```

### Token Storage

- **Access Token:** `localStorage.getItem('access_token')`
- **Refresh Token:** `localStorage.getItem('refresh_token')`

Tokens are automatically included in API requests via axios interceptor.

### Auto Token Refresh

- Tokens are automatically refreshed on 401 responses
- Background refresh every 20 hours
- Seamless user experience

## Setup Instructions

### Backend Setup

1. **Install dependencies:**
```bash
cd fastapi-backend
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
# Generate secret key
openssl rand -hex 32

# Add to .env
JWT_SECRET_KEY=<generated-secret-key>
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/apartment_db
```

3. **Run database migration:**
```bash
psql -U postgres -d apartment_db -f migrations/001_create_auth_tables.sql
```

4. **Start server:**
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd nextjs-frontend
npm install
```

2. **Set environment variables:**
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Start development server:**
```bash
npm run dev
```

## Testing

### Manual Testing

1. **Register a new user:**
   - Visit http://localhost:3000/register
   - Fill in the form
   - Should redirect to home page after registration

2. **Login:**
   - Visit http://localhost:3000/login
   - Enter credentials
   - Should redirect to home page after login

3. **View profile:**
   - Visit http://localhost:3000/profile
   - Should see user details and subscription info

4. **Logout:**
   - Click logout button
   - Should redirect to login page

### API Testing with cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234",
    "confirm_password": "Test1234",
    "name": "Test User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234"
  }'
```

**Get Profile:**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## Subscription Tiers

### Free Tier (Default)
- 100 API calls per hour
- Basic analytics access
- Limited features

### Premium Tier
- 1000 API calls per hour
- Advanced analytics
- Premium features
- Priority support

### Enterprise Tier
- Unlimited API calls
- Custom analytics
- All features
- Dedicated support

## Next Steps (Not Yet Implemented)

1. **Payment Integration:** Connect subscription upgrades to payment gateway
2. **Email Verification:** Send verification emails on registration
3. **Password Reset:** Implement forgot password flow
4. **OAuth Integration:** Google/GitHub social login
5. **Two-Factor Authentication:** Optional 2FA for enhanced security
6. **API Key Management:** Generate API keys for programmatic access
7. **Usage Analytics:** Track API usage per user
8. **Admin Dashboard:** Manage users and subscriptions

## Security Considerations

1. **Never commit** `.env` files with real secrets
2. **Rotate JWT secrets** regularly in production
3. **Use HTTPS** in production
4. **Enable CSRF protection** for forms
5. **Implement rate limiting** on all endpoints
6. **Log authentication events** for security monitoring
7. **Use secure cookie flags** when appropriate
8. **Validate all user input** on both frontend and backend

## Troubleshooting

### Token expired error
- Tokens are automatically refreshed
- If refresh fails, user is logged out
- Check refresh token expiry (7 days)

### CORS errors
- Verify `CORS_ORIGINS` in backend middleware
- Check `NEXT_PUBLIC_API_URL` in frontend

### Rate limit exceeded
- Check rate limiter configuration
- Verify user tier limits
- Consider implementing Redis for distributed rate limiting

### Database connection errors
- Verify `DATABASE_URL` is correct
- Check PostgreSQL is running
- Verify migrations have been applied

## Production Deployment

### Backend
1. Set secure `JWT_SECRET_KEY`
2. Use production database
3. Enable HTTPS
4. Configure proper CORS origins
5. Set up monitoring and logging

### Frontend
1. Set production `NEXT_PUBLIC_API_URL`
2. Build for production: `npm run build`
3. Deploy to Vercel/Netlify
4. Configure environment variables

## License

Copyright © 2026 Apartment Analysis Platform
