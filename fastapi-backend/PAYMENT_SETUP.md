# Payment Integration Setup

## Quick Start

### 1. Environment Variables

Copy `.env.example` to `.env` and ensure payment variables are set:

```env
PORTONE_API_KEY=test_key
PORTONE_API_SECRET=test_secret
PORTONE_WEBHOOK_SECRET=test_webhook_secret
PAYMENT_MODE=mock  # mock for development, production for real payments
```

### 2. Database Migration

Run the payment table migration:

```bash
cd fastapi-backend
python -m auth.migrate_payments
```

This creates the `payments` table with:
- Payment records (amount, status, receipt numbers)
- Foreign key to users table
- Indexes for performance
- Payment status enum type

### 3. Verify Migration

Check that the table was created:

```bash
psql -d apartment_db -c "\d payments"
```

### 4. Start Backend

```bash
uvicorn main:app --reload
```

### 5. Test Payment Endpoints

Visit API documentation:
```
http://localhost:8000/docs
```

Navigate to **payments** section to test:
- POST `/api/v1/payments/create` - Create payment
- POST `/api/v1/payments/verify` - Verify payment
- GET `/api/v1/payments/history` - Get payment history

## Testing Mock Payments

### Create Payment

```bash
curl -X POST http://localhost:8000/api/v1/payments/create \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 9900,
    "currency": "KRW",
    "payment_method": "card"
  }'
```

Response:
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

### Verify Payment

```bash
curl -X POST http://localhost:8000/api/v1/payments/verify \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "portone_payment_id": "mock_pay_20260208_abcd1234"
  }'
```

Response (after 2-second delay):
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

## Mock Payment Behavior

- **All payments succeed** (100% success rate)
- **2-second processing delay** simulates real payment gateway
- **Receipt numbers generated** in format `RCP{YYYYMMDD}-{RANDOM}`
- **Subscription automatically activated** for 30 days
- **Webhook signature verification** always passes

## Database Schema

### payments Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK to users.id |
| amount | NUMERIC(10,2) | Payment amount |
| currency | VARCHAR(3) | Currency code (default: KRW) |
| status | payment_status | pending, processing, completed, failed, refunded |
| payment_method | VARCHAR(50) | card, bank_transfer |
| portone_payment_id | VARCHAR(100) | PortOne gateway ID (unique) |
| receipt_number | VARCHAR(100) | Receipt number (unique) |
| created_at | TIMESTAMP | Creation time |
| completed_at | TIMESTAMP | Completion time |

## Rollback Migration

If you need to remove the payments table:

```bash
python -m auth.migrate_payments --rollback
```

**Warning:** This will delete all payment records!

## Production Deployment

See [PAYMENT_INTEGRATION.md](../PAYMENT_INTEGRATION.md) for:
- Switching from mock to production mode
- Real PortOne API integration
- Webhook signature verification
- Security checklist
- Monitoring and logging

## Troubleshooting

### Migration fails with "relation already exists"

The table already exists. Either:
1. Drop it manually: `DROP TABLE payments CASCADE;`
2. Or skip migration if structure is correct

### Payment verify takes too long

This is expected in mock mode (2-second delay). In production, actual PortOne API calls may take 1-5 seconds.

### JWT token invalid

Ensure you're using a valid access token:
```bash
# Login first
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use the access_token from response
```

## Support

- API Documentation: http://localhost:8000/docs
- Full Guide: [PAYMENT_INTEGRATION.md](../PAYMENT_INTEGRATION.md)
- Backend Issues: Check logs in console
