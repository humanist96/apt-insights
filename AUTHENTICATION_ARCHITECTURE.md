# Authentication System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Next.js Frontend (Port 3000)                 │   │
│  │                                                            │   │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │   │
│  │  │Login Page  │  │Register Page │  │  Profile Page   │  │   │
│  │  └────────────┘  └──────────────┘  └─────────────────┘  │   │
│  │         │                │                    │           │   │
│  │         └────────────────┴────────────────────┘           │   │
│  │                          │                                │   │
│  │                 ┌────────▼────────┐                       │   │
│  │                 │  Auth Context   │                       │   │
│  │                 │  (State Mgmt)   │                       │   │
│  │                 └────────┬────────┘                       │   │
│  │                          │                                │   │
│  │                 ┌────────▼────────┐                       │   │
│  │                 │   API Client    │                       │   │
│  │                 │  (Axios + JWT)  │                       │   │
│  │                 └────────┬────────┘                       │   │
│  └──────────────────────────┼──────────────────────────────┘   │
└────────────────────────────┼──────────────────────────────────┘
                             │
                    HTTPS (JWT Bearer Token)
                             │
┌────────────────────────────▼──────────────────────────────────┐
│              FastAPI Backend (Port 8000)                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                   Middleware Layer                        │ │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │ │
│  │  │    CORS    │→ │ Rate Limiter │→ │    Logging      │  │ │
│  │  └────────────┘  └──────────────┘  └─────────────────┘  │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │               Auth Router (/api/v1/auth)                  │ │
│  │                                                            │ │
│  │  POST /register    POST /login     POST /refresh          │ │
│  │  GET  /me          PUT  /me        POST /logout           │ │
│  │                                                            │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │            Auth Dependencies Layer                   │ │ │
│  │  │  ┌──────────────┐  ┌───────────────────────────┐   │ │ │
│  │  │  │get_current_  │  │   require_premium()       │   │ │ │
│  │  │  │    user()    │  │                           │   │ │ │
│  │  │  └──────────────┘  └───────────────────────────┘   │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │                    JWT Service Layer                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │   Create     │  │    Verify    │  │   Password   │   │ │
│  │  │   Tokens     │  │    Tokens    │  │    Hash      │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │              SQLAlchemy ORM Layer                         │ │
│  │  ┌──────────────┐            ┌──────────────┐            │ │
│  │  │ User Model   │            │Subscription  │            │ │
│  │  │              │            │   Model      │            │ │
│  │  └──────────────┘            └──────────────┘            │ │
│  └──────────────────────────┬───────────────────────────────┘ │
└────────────────────────────┼──────────────────────────────────┘
                             │
                    PostgreSQL Connection
                             │
┌────────────────────────────▼──────────────────────────────────┐
│                  PostgreSQL Database                           │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ┌─────────────────┐         ┌──────────────────────┐   │ │
│  │  │  users table    │  1:N    │ subscriptions table  │   │ │
│  │  │                 │────────▶│                      │   │ │
│  │  │  • id           │         │  • id                │   │ │
│  │  │  • email        │         │  • user_id (FK)      │   │ │
│  │  │  • password_hash│         │  • plan              │   │ │
│  │  │  • name         │         │  • amount            │   │ │
│  │  │  • tier         │         │  • started_at        │   │ │
│  │  │  • expires_at   │         │  • expires_at        │   │ │
│  │  │  • created_at   │         │  • status            │   │ │
│  │  │  • last_login   │         │                      │   │ │
│  │  └─────────────────┘         └──────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

## Authentication Flow

### Registration Flow

```
User                Frontend              Backend                Database
 │                     │                     │                      │
 │ Fill form           │                     │                      │
 ├────────────────────▶│                     │                      │
 │                     │                     │                      │
 │                     │ POST /register      │                      │
 │                     ├────────────────────▶│                      │
 │                     │ {email, password}   │                      │
 │                     │                     │                      │
 │                     │                     │ Validate input       │
 │                     │                     │ Hash password        │
 │                     │                     │                      │
 │                     │                     │ INSERT INTO users    │
 │                     │                     ├─────────────────────▶│
 │                     │                     │                      │
 │                     │                     │◀─────────────────────┤
 │                     │                     │ User created         │
 │                     │                     │                      │
 │                     │                     │ Create JWT tokens    │
 │                     │                     │                      │
 │                     │◀────────────────────┤                      │
 │                     │ {access_token,      │                      │
 │                     │  refresh_token}     │                      │
 │                     │                     │                      │
 │ Store tokens        │                     │                      │
 │◀────────────────────┤                     │                      │
 │ Redirect to home    │                     │                      │
 │                     │                     │                      │
```

### Login Flow

```
User                Frontend              Backend                Database
 │                     │                     │                      │
 │ Enter credentials   │                     │                      │
 ├────────────────────▶│                     │                      │
 │                     │                     │                      │
 │                     │ POST /login         │                      │
 │                     ├────────────────────▶│                      │
 │                     │ {email, password}   │                      │
 │                     │                     │                      │
 │                     │                     │ SELECT FROM users    │
 │                     │                     ├─────────────────────▶│
 │                     │                     │                      │
 │                     │                     │◀─────────────────────┤
 │                     │                     │ User data            │
 │                     │                     │                      │
 │                     │                     │ Verify password      │
 │                     │                     │ Update last_login    │
 │                     │                     │ Create JWT tokens    │
 │                     │                     │                      │
 │                     │◀────────────────────┤                      │
 │                     │ {access_token,      │                      │
 │                     │  refresh_token}     │                      │
 │                     │                     │                      │
 │ Store tokens        │                     │                      │
 │◀────────────────────┤                     │                      │
 │ Redirect to home    │                     │                      │
 │                     │                     │                      │
```

### Protected Route Access Flow

```
User                Frontend              Backend                Database
 │                     │                     │                      │
 │ Access /profile     │                     │                      │
 ├────────────────────▶│                     │                      │
 │                     │                     │                      │
 │                     │ Check auth state    │                      │
 │                     │                     │                      │
 │                     │ GET /me             │                      │
 │                     ├────────────────────▶│                      │
 │                     │ Authorization:      │                      │
 │                     │ Bearer <token>      │                      │
 │                     │                     │                      │
 │                     │                     │ Verify JWT           │
 │                     │                     │                      │
 │                     │                     │ SELECT FROM users    │
 │                     │                     ├─────────────────────▶│
 │                     │                     │                      │
 │                     │                     │◀─────────────────────┤
 │                     │                     │ User data            │
 │                     │                     │                      │
 │                     │◀────────────────────┤                      │
 │                     │ User profile        │                      │
 │                     │                     │                      │
 │ Display profile     │                     │                      │
 │◀────────────────────┤                     │                      │
 │                     │                     │                      │
```

### Token Refresh Flow

```
Frontend              Backend                Database
    │                     │                      │
    │ Access token        │                      │
    │ expired (401)       │                      │
    │                     │                      │
    │ POST /refresh       │                      │
    ├────────────────────▶│                      │
    │ {refresh_token}     │                      │
    │                     │                      │
    │                     │ Verify refresh token │
    │                     │                      │
    │                     │ SELECT FROM users    │
    │                     ├─────────────────────▶│
    │                     │                      │
    │                     │◀─────────────────────┤
    │                     │ User data            │
    │                     │                      │
    │                     │ Create new tokens    │
    │                     │                      │
    │◀────────────────────┤                      │
    │ {new_access_token,  │                      │
    │  new_refresh_token} │                      │
    │                     │                      │
    │ Retry original      │                      │
    │ request             │                      │
    │                     │                      │
```

## Component Dependencies

```
┌────────────────────────────────────────────────────────────┐
│                      Frontend Layer                        │
│                                                             │
│  AuthContext                                               │
│     ↓                                                       │
│  AuthProvider ────▶ API Client ────▶ axios                │
│     ↓                                                       │
│  Auth Pages                                                │
│     • Login                                                │
│     • Register                                             │
│     • Profile                                              │
│     ↓                                                       │
│  Components                                                │
│     • ProtectedRoute                                       │
│     • AuthNav                                              │
└────────────────────────────────────────────────────────────┘
                              ↓ HTTP
┌────────────────────────────────────────────────────────────┐
│                      Backend Layer                         │
│                                                             │
│  main.py ────▶ Middleware ────▶ Auth Router               │
│                  • CORS                                    │
│                  • Rate Limiter                            │
│                  • Logging                                 │
│                       ↓                                     │
│  Auth Module                                               │
│     • router.py ────▶ dependencies.py ────▶ jwt.py        │
│                           ↓                                │
│                       models.py                            │
│                           ↓                                │
│                       database.py                          │
└────────────────────────────────────────────────────────────┘
                              ↓ SQL
┌────────────────────────────────────────────────────────────┐
│                      Database Layer                        │
│                                                             │
│  PostgreSQL                                                │
│     • users table                                          │
│     • subscriptions table                                  │
└────────────────────────────────────────────────────────────┘
```

## Data Models

### User Model

```typescript
interface User {
  id: number;
  email: string;
  password_hash: string;        // Backend only
  name?: string;
  subscription_tier: 'free' | 'premium' | 'enterprise';
  subscription_expires_at?: Date;
  created_at: Date;
  last_login_at?: Date;
}
```

### Subscription Model

```typescript
interface Subscription {
  id: number;
  user_id: number;
  plan: string;
  amount: number;
  started_at: Date;
  expires_at?: Date;
  status: 'active' | 'expired' | 'cancelled';
}
```

### Token Response

```typescript
interface Token {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}
```

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Client Side                          │
│                                                          │
│  • Input validation (TypeScript)                        │
│  • Password strength check                              │
│  • Email format validation                              │
│  • Secure token storage (localStorage)                  │
└────────────────────┬────────────────────────────────────┘
                     │
                HTTPS (TLS)
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Network Layer                          │
│                                                          │
│  • CORS protection                                      │
│  • Rate limiting (IP-based)                             │
│  • Request logging                                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               Application Layer                         │
│                                                          │
│  • JWT verification                                     │
│  • Pydantic validation                                  │
│  • Business logic checks                                │
│  • Bcrypt password hashing                              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Database Layer                          │
│                                                          │
│  • SQL injection prevention (ORM)                       │
│  • Foreign key constraints                              │
│  • Unique constraints                                   │
│  • Indexes for performance                              │
└─────────────────────────────────────────────────────────┘
```

## Token Lifecycle

```
┌──────────┐
│  Login   │
└────┬─────┘
     │
     ▼
┌──────────────────────────┐
│  Generate Tokens         │
│  • Access (24h)          │
│  • Refresh (7d)          │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Store in localStorage   │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Use Access Token        │
│  (API requests)          │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Token Expired?          │
└────┬──────────┬──────────┘
     │          │
    No         Yes
     │          │
     ▼          ▼
┌─────────┐  ┌──────────────┐
│Continue │  │Auto Refresh  │
└─────────┘  │w/ Refresh    │
             │Token         │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │New Tokens    │
             │Generated     │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │Retry Request │
             └──────────────┘
```

## Rate Limiting Architecture

```
┌───────────────────────────────────────────────────────┐
│                 Incoming Request                      │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Extract Client IP     │
         └───────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │ Check Authentication       │
    └─────┬───────────┬──────────┘
          │           │
      Authenticated  Anonymous
          │           │
          ▼           ▼
   ┌──────────┐  ┌──────────┐
   │Premium:  │  │Free:     │
   │Unlimited │  │100/hour  │
   └────┬─────┘  └────┬─────┘
        │             │
        └──────┬──────┘
               │
               ▼
    ┌──────────────────────┐
    │ Check Request Count  │
    │ in Time Window       │
    └─────┬────────┬───────┘
          │        │
      Allowed   Exceeded
          │        │
          ▼        ▼
    ┌─────────┐ ┌─────────┐
    │Process  │ │Return   │
    │Request  │ │429 Error│
    └─────────┘ └─────────┘
```

## File Organization

```
Backend Structure:
auth/
├── __init__.py          # Exports: auth_router, get_current_user, require_premium
├── database.py          # SQLAlchemy setup, session management
├── models.py            # User, Subscription models
├── schemas.py           # Pydantic schemas with validators
├── jwt.py               # Token creation, verification, password hashing
├── dependencies.py      # FastAPI dependencies for auth
└── router.py            # API endpoints

Frontend Structure:
contexts/
└── AuthContext.tsx      # Global auth state

app/
├── login/page.tsx       # Login form
├── register/page.tsx    # Registration form
└── profile/page.tsx     # User profile

components/
├── ProtectedRoute.tsx   # Route guard
└── AuthNav.tsx          # Navigation
```

---

This architecture provides a robust, scalable, and secure authentication system following industry best practices and modern web development standards.
