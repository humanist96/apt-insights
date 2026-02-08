# Payment Integration - Quick Reference

## Setup (5 Minutes)

### 1. Backend Setup
```bash
cd fastapi-backend

# Set environment variables
cp .env.example .env
# Edit .env - ensure PAYMENT_MODE=mock

# Run migration
python -m auth.migrate_payments

# Test service
python test_payment_integration.py

# Start server
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd nextjs-frontend

# Ensure .env.local has API URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

## Test Payment Flow (2 Minutes)

1. **Navigate to payment page**: http://localhost:3000/payment
2. **Enter test data**:
   - Card: `1234 5678 9012 3456` (any 16 digits)
   - Expiry: `12/26` (any future date)
   - CVV: `123` (any 3 digits)
   - Check "Agree to terms"
3. **Submit** and wait 2 seconds
4. **Verify** success page shows receipt number

## API Quick Test

```bash
# Get JWT token first
TOKEN="your_jwt_token_here"

# Create payment
curl -X POST http://localhost:8000/api/v1/payments/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 9900, "currency": "KRW", "payment_method": "card"}'

# Save the portone_payment_id from response

# Verify payment
curl -X POST http://localhost:8000/api/v1/payments/verify \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"portone_payment_id": "mock_pay_20260208_abcd1234"}'

# Check payment history
curl -X GET http://localhost:8000/api/v1/payments/history \
  -H "Authorization: Bearer $TOKEN"
```

## Key Files

### Backend
- **Models**: `fastapi-backend/auth/models.py`
- **Service**: `fastapi-backend/services/payment_service.py`
- **Router**: `fastapi-backend/routers/payment.py`
- **Migration**: `fastapi-backend/auth/migrate_payments.py`

### Frontend
- **Payment Form**: `nextjs-frontend/app/payment/page.tsx`
- **Success**: `nextjs-frontend/app/payment/success/page.tsx`
- **Failure**: `nextjs-frontend/app/payment/failure/page.tsx`

## Mock Behavior

| Feature | Mock Behavior |
|---------|---------------|
| Payment Success Rate | 100% |
| Processing Time | 2 seconds |
| Receipt Format | `RCP{YYYYMMDD}-{HEX}` |
| Card Validation | Accept any 16 digits |
| Subscription | Auto-activate for 30 days |

## Environment Variables

```env
# Backend
PAYMENT_MODE=mock
PORTONE_API_KEY=test_key
PORTONE_API_SECRET=test_secret
PORTONE_WEBHOOK_SECRET=test_webhook_secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Common Issues

### "Payment not found"
- Ensure you're using the correct `portone_payment_id` from create response
- Check that payment was created with same user's JWT token

### "JWT token invalid"
- Get fresh token by logging in
- Ensure token is passed in Authorization header

### Migration fails
- Check DATABASE_URL is correct
- Verify PostgreSQL is running
- Table may already exist (safe to skip)

### Frontend can't connect to API
- Verify backend is running on port 8000
- Check NEXT_PUBLIC_API_URL is correct
- Check CORS settings in backend

## Switch to Production

```env
# Change in .env
PAYMENT_MODE=production

# Add real credentials
PORTONE_API_KEY=real_key_from_portone
PORTONE_API_SECRET=real_secret_from_portone
PORTONE_WEBHOOK_SECRET=real_webhook_secret
```

Then implement real API calls in `payment_service.py`.

## Documentation

- **Full Guide**: [PAYMENT_INTEGRATION.md](./PAYMENT_INTEGRATION.md)
- **Setup**: [fastapi-backend/PAYMENT_SETUP.md](./fastapi-backend/PAYMENT_SETUP.md)
- **Summary**: [PAYMENT_IMPLEMENTATION_SUMMARY.md](./PAYMENT_IMPLEMENTATION_SUMMARY.md)
- **API Docs**: http://localhost:8000/docs

## Support

- Check logs in terminal for errors
- Use test script: `python test_payment_integration.py`
- Check API docs: http://localhost:8000/docs
- Review error messages in browser console

---

**Quick Start**: Backend setup → Frontend setup → Test payment → Done!
