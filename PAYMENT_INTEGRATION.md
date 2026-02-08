# Payment Integration Guide

## Overview

This document describes the payment integration foundation for the apartment transaction analysis platform. The system is designed with **mock PortOne implementation** for development and testing, with a clear path to production deployment.

## Architecture

### Backend (FastAPI)

```
fastapi-backend/
├── auth/
│   └── models.py           # Payment, PaymentStatus models
├── schemas/
│   └── payment.py          # Payment request/response schemas
├── services/
│   └── payment_service.py  # Mock PortOne service
└── routers/
    └── payment.py          # Payment API endpoints
```

### Frontend (Next.js)

```
nextjs-frontend/app/
├── payment/
│   ├── page.tsx           # Payment form
│   ├── success/
│   │   └── page.tsx       # Success page
│   └── failure/
│       └── page.tsx       # Failure page
└── profile/
    └── (subscription settings in profile page)
```

## Payment Flow

### 1. Mock Payment Flow (Development)

```
User → Payment Page → Enter Card Info → Submit
  ↓
Create Payment Intent (POST /api/v1/payments/create)
  ↓
2-Second Processing Delay (simulates real payment)
  ↓
Verify Payment (POST /api/v1/payments/verify)
  ↓
Activate Subscription (update user tier, expires_at)
  ↓
Success Page with Receipt Number
```

### 2. Production Payment Flow (Future)

```
User → Payment Page → Submit
  ↓
Create Payment Intent with Real PortOne API
  ↓
Redirect to PortOne Payment Gateway
  ↓
User Completes Payment on PortOne
  ↓
PortOne Webhook Notification
  ↓
Verify Webhook Signature
  ↓
Update Payment Status → Activate Subscription
  ↓
Success Page
```

## API Endpoints

### POST `/api/v1/payments/create`

Create a payment intent.

**Request:**
```json
{
  "amount": 9900,
  "currency": "KRW",
  "payment_method": "card"
}
```

**Response:**
```json
{
  "success": true,
  "payment_id": "1",
  "portone_payment_id": "mock_pay_20260208_abcd1234",
  "amount": 9900,
  "currency": "KRW",
  "status": "pending",
  "created_at": "2026-02-08T12:00:00"
}
```

### POST `/api/v1/payments/verify`

Verify payment and activate subscription.

**Request:**
```json
{
  "portone_payment_id": "mock_pay_20260208_abcd1234",
  "webhook_signature": "mock_signature_xyz"
}
```

**Response:**
```json
{
  "success": true,
  "payment_id": "1",
  "status": "completed",
  "receipt_number": "RCP20260208-ABC123",
  "completed_at": "2026-02-08T12:00:05",
  "subscription_activated": true,
  "subscription_expires_at": "2026-03-08T12:00:05"
}
```

### GET `/api/v1/payments/history`

Get payment history for current user.

**Query Parameters:**
- `limit` (optional, default: 50): Maximum number of records
- `offset` (optional, default: 0): Number of records to skip

**Response:**
```json
{
  "success": true,
  "total": 2,
  "payments": [
    {
      "id": 1,
      "amount": 9900,
      "currency": "KRW",
      "status": "completed",
      "payment_method": "card",
      "receipt_number": "RCP20260208-ABC123",
      "created_at": "2026-02-08T12:00:00",
      "completed_at": "2026-02-08T12:00:05"
    }
  ]
}
```

### POST `/api/v1/payments/webhook`

Webhook endpoint for PortOne payment notifications (production only).

**Request:**
```json
{
  "payment_id": "mock_pay_20260208_abcd1234",
  "status": "completed",
  "amount": 9900,
  "currency": "KRW",
  "receipt_number": "RCP20260208-ABC123",
  "signature": "mock_signature_xyz"
}
```

## Database Schema

### payments Table

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount NUMERIC(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'KRW' NOT NULL,
    status VARCHAR(20) NOT NULL,  -- pending, processing, completed, failed, refunded
    payment_method VARCHAR(50),
    portone_payment_id VARCHAR(100) UNIQUE,
    receipt_number VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    completed_at TIMESTAMP,

    INDEX idx_user_payments (user_id),
    INDEX idx_portone_payment (portone_payment_id),
    INDEX idx_status (status)
);
```

### Subscription Activation

When payment is verified:
1. Update `users.subscription_tier` → `premium`
2. Set `users.subscription_expires_at` → 30 days from now
3. Create `subscriptions` record with `ACTIVE` status

## Environment Variables

### Backend (.env)

```env
# Payment Integration (PortOne)
PORTONE_API_KEY=test_key
PORTONE_API_SECRET=test_secret
PORTONE_WEBHOOK_SECRET=test_webhook_secret
PAYMENT_MODE=mock  # mock or production
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Mock Payment Testing

### Test Card Numbers (Mock Mode)

In mock mode, **any 16-digit number** is accepted:

- `1234 5678 9012 3456` - Always succeeds
- `4111 1111 1111 1111` - Always succeeds
- Any other 16 digits - Always succeeds

**Expiry Date:** Any future date (MM/YY format)
**CVV:** Any 3 digits

### Mock Behavior

- **Processing Delay:** 2 seconds (simulates real payment gateway)
- **Success Rate:** 100% (all payments succeed)
- **Receipt Numbers:** Generated as `RCP{YYYYMMDD}-{RANDOM_HEX}`
- **Webhook Signature:** Always validates as true

## Switching to Production

### Step 1: Obtain PortOne Credentials

1. Sign up at [PortOne](https://portone.io/)
2. Get API credentials:
   - `PORTONE_API_KEY`
   - `PORTONE_API_SECRET`
   - `PORTONE_WEBHOOK_SECRET`

### Step 2: Update Environment Variables

```env
PORTONE_API_KEY=your_real_api_key
PORTONE_API_SECRET=your_real_api_secret
PORTONE_WEBHOOK_SECRET=your_real_webhook_secret
PAYMENT_MODE=production  # Change from mock to production
```

### Step 3: Implement Real PortOne Integration

Update `/fastapi-backend/services/payment_service.py`:

```python
async def create_payment_intent(self, ...):
    if self.payment_mode == "production":
        # Implement real PortOne API call
        response = await httpx.post(
            "https://api.portone.io/v1/payments",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "amount": float(amount),
                "currency": currency,
                "payment_method": payment_method,
                # ... other PortOne-specific fields
            }
        )
        return response.json()
```

### Step 4: Configure Webhook URL

In PortOne dashboard, set webhook URL:
```
https://your-domain.com/api/v1/payments/webhook
```

### Step 5: Implement Signature Verification

```python
def verify_webhook_signature(self, payload: dict, signature: str) -> bool:
    if self.payment_mode == "production":
        import hmac
        import hashlib

        payload_str = json.dumps(payload, sort_keys=True)
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)
    return True  # Mock mode
```

## Security Considerations

### Backend Security

1. **Authentication Required:** All payment endpoints require valid JWT token
2. **User Verification:** Payment records are tied to authenticated user
3. **Input Validation:** All inputs validated with Pydantic schemas
4. **Error Handling:** Sensitive error details not exposed to client
5. **Database Transactions:** Atomic payment + subscription updates

### Frontend Security

1. **No Sensitive Data Storage:** Card details never stored
2. **HTTPS Only:** Production must use HTTPS
3. **Token Management:** JWT tokens stored in localStorage
4. **CORS Protection:** Backend CORS configured for specific origins

### Production Checklist

- [ ] Replace mock PortOne service with real implementation
- [ ] Configure webhook signature verification
- [ ] Set up HTTPS for frontend and backend
- [ ] Enable rate limiting on payment endpoints
- [ ] Set up monitoring and alerting
- [ ] Test with PortOne sandbox environment
- [ ] Implement payment retry logic
- [ ] Add payment timeout handling
- [ ] Configure error reporting (Sentry, etc.)
- [ ] Set up payment reconciliation process

## Error Handling

### Common Errors

| Error Code | Description | Resolution |
|------------|-------------|------------|
| 401 | Unauthorized | User not authenticated, redirect to login |
| 404 | Payment not found | Payment record doesn't exist |
| 500 | Internal server error | Log error, show generic message to user |

### Frontend Error Display

```typescript
try {
  // Payment logic
} catch (err) {
  setError(err.response?.data?.detail || "결제 처리 중 오류가 발생했습니다");
}
```

## Testing

### Manual Testing (Mock Mode)

1. **Start Backend:**
   ```bash
   cd fastapi-backend
   uvicorn main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd nextjs-frontend
   npm run dev
   ```

3. **Test Payment Flow:**
   - Navigate to `/payment`
   - Enter any 16-digit card number
   - Enter any future expiry date (MM/YY)
   - Enter any 3-digit CVV
   - Check "Agree to terms"
   - Click "결제하기"
   - Wait 2 seconds for processing
   - Verify redirect to success page

4. **Test Payment History:**
   - Navigate to `/profile`
   - View subscription settings
   - See payment history

### API Testing (cURL)

```bash
# Create payment
curl -X POST http://localhost:8000/api/v1/payments/create \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 9900, "currency": "KRW", "payment_method": "card"}'

# Verify payment
curl -X POST http://localhost:8000/api/v1/payments/verify \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"portone_payment_id": "mock_pay_20260208_abcd1234"}'

# Get payment history
curl -X GET http://localhost:8000/api/v1/payments/history \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Subscription Management

### Activation Flow

1. Payment verified successfully
2. User subscription_tier updated to `premium`
3. User subscription_expires_at set to +30 days
4. Subscription record created with:
   - `plan`: "premium_monthly"
   - `amount`: 9900
   - `status`: ACTIVE
   - `expires_at`: +30 days

### Expiration Handling

Implement a daily cron job to:
1. Find users with `subscription_expires_at < NOW()`
2. Update `subscription_tier` → `free`
3. Update subscription status → `EXPIRED`

### Cancellation Flow

1. User clicks "구독 취소" in profile
2. POST to `/api/v1/subscriptions/cancel`
3. Update subscription status → `CANCELLED`
4. Allow access until `subscription_expires_at`

## Price Plans

### Current Plan

| Plan | Price | Duration | Features |
|------|-------|----------|----------|
| Premium Monthly | ₩9,900 | 30 days | Unlimited data, CSV/PDF export, Premium analysis |

### Future Plans (To Implement)

- Premium Quarterly: ₩27,000 (10% discount)
- Premium Annual: ₩99,000 (17% discount)
- Enterprise: Custom pricing

## Monitoring

### Key Metrics to Track

1. **Payment Success Rate:** `completed / total * 100`
2. **Average Processing Time:** Time from create to verify
3. **Failed Payments:** Count and reasons
4. **Active Subscriptions:** Count of ACTIVE subscriptions
5. **Revenue:** Sum of completed payments
6. **Churn Rate:** Cancelled subscriptions / total

### Logging

All payment operations are logged with structured logging:

```python
logger.info(
    "payment_verified_subscription_activated",
    payment_id=payment.id,
    user_id=current_user.id,
    subscription_expires_at=subscription_expires_at.isoformat()
)
```

## Support

For issues or questions:
- **Email:** support@example.com
- **Documentation:** See API docs at `/docs`
- **PortOne Support:** https://portone.io/support

---

**Last Updated:** 2026-02-08
**Version:** 1.0.0
**Status:** Mock Implementation (Production-Ready Structure)
