#!/bin/bash

# Authentication System Verification Script
# Checks that all components are properly installed

set -e

echo "==========================================="
echo "Authentication System Verification"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Backend checks
echo "Backend Components:"
echo "-------------------"

# Check auth module files
for file in __init__.py database.py models.py schemas.py jwt.py dependencies.py router.py; do
    if [ -f "fastapi-backend/auth/$file" ]; then
        check_pass "fastapi-backend/auth/$file exists"
    else
        check_fail "fastapi-backend/auth/$file missing"
    fi
done

# Check middleware
if [ -f "fastapi-backend/middleware/rate_limiter.py" ]; then
    check_pass "Rate limiter middleware exists"
else
    check_fail "Rate limiter middleware missing"
fi

# Check migration
if [ -f "fastapi-backend/migrations/001_create_auth_tables.sql" ]; then
    check_pass "Database migration exists"
else
    check_fail "Database migration missing"
fi

# Check test script
if [ -f "fastapi-backend/test_auth.py" ]; then
    check_pass "Test script exists"
else
    check_fail "Test script missing"
fi

# Check dependencies
if grep -q "passlib" fastapi-backend/requirements.txt; then
    check_pass "Auth dependencies in requirements.txt"
else
    check_fail "Auth dependencies missing from requirements.txt"
fi

# Check .env configuration
if [ -f "fastapi-backend/.env" ]; then
    if grep -q "JWT_SECRET_KEY" fastapi-backend/.env; then
        check_pass "JWT secret key configured"
    else
        check_warn "JWT secret key not found in .env"
    fi
else
    check_warn ".env file not found (run setup_auth.sh)"
fi

echo ""
echo "Frontend Components:"
echo "--------------------"

# Check context
if [ -f "nextjs-frontend/contexts/AuthContext.tsx" ]; then
    check_pass "Auth context exists"
else
    check_fail "Auth context missing"
fi

# Check pages
for page in login register profile; do
    if [ -f "nextjs-frontend/app/$page/page.tsx" ]; then
        check_pass "$page page exists"
    else
        check_fail "$page page missing"
    fi
done

# Check components
for component in ProtectedRoute.tsx AuthNav.tsx; do
    if [ -f "nextjs-frontend/components/$component" ]; then
        check_pass "$component exists"
    else
        check_fail "$component missing"
    fi
done

# Check providers
if grep -q "AuthProvider" nextjs-frontend/app/providers.tsx; then
    check_pass "AuthProvider integrated"
else
    check_fail "AuthProvider not integrated"
fi

# Check environment
if [ -f "nextjs-frontend/.env.local" ]; then
    check_pass "Frontend .env.local exists"
else
    check_warn "Frontend .env.local not found (run setup_auth.sh)"
fi

echo ""
echo "Documentation:"
echo "--------------"

for doc in AUTHENTICATION.md AUTHENTICATION_QUICKSTART.md AUTHENTICATION_IMPLEMENTATION_SUMMARY.md; do
    if [ -f "$doc" ]; then
        check_pass "$doc exists"
    else
        check_fail "$doc missing"
    fi
done

echo ""
echo "Scripts:"
echo "--------"

if [ -f "scripts/setup_auth.sh" ] && [ -x "scripts/setup_auth.sh" ]; then
    check_pass "setup_auth.sh exists and is executable"
else
    check_fail "setup_auth.sh missing or not executable"
fi

echo ""
echo "Database:"
echo "---------"

# Check PostgreSQL
if command -v psql &> /dev/null; then
    check_pass "PostgreSQL client installed"

    if pg_isready -q; then
        check_pass "PostgreSQL server is running"

        # Check if auth tables exist
        DB_NAME=$(grep DATABASE_URL .env 2>/dev/null | cut -d '/' -f 4 | cut -d '?' -f 1 || echo "apartment_db")
        DB_USER=$(grep DATABASE_URL .env 2>/dev/null | cut -d '@' -f 1 | cut -d '/' -f 3 | cut -d ':' -f 1 || echo "postgres")

        if psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1 FROM users LIMIT 1;" &> /dev/null; then
            check_pass "Users table exists"
        else
            check_warn "Users table not found (run migration)"
        fi

        if psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1 FROM subscriptions LIMIT 1;" &> /dev/null; then
            check_pass "Subscriptions table exists"
        else
            check_warn "Subscriptions table not found (run migration)"
        fi
    else
        check_warn "PostgreSQL server is not running"
    fi
else
    check_fail "PostgreSQL client not installed"
fi

echo ""
echo "Python Dependencies:"
echo "--------------------"

cd fastapi-backend

if python -c "import passlib" 2>/dev/null; then
    check_pass "passlib installed"
else
    check_warn "passlib not installed (run: pip install -r requirements.txt)"
fi

if python -c "import jose" 2>/dev/null; then
    check_pass "python-jose installed"
else
    check_warn "python-jose not installed (run: pip install -r requirements.txt)"
fi

cd ..

echo ""
echo "Node.js Dependencies:"
echo "---------------------"

cd nextjs-frontend

if [ -d "node_modules" ]; then
    check_pass "node_modules exists"
else
    check_warn "node_modules not found (run: npm install)"
fi

cd ..

echo ""
echo "==========================================="
echo "Verification Results"
echo "==========================================="
echo ""
echo -e "${GREEN}Passed:${NC} $PASS"
echo -e "${RED}Failed:${NC} $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Authentication system is properly installed."
    echo ""
    echo "Next steps:"
    echo "1. Start backend: cd fastapi-backend && uvicorn main:app --reload"
    echo "2. Start frontend: cd nextjs-frontend && npm run dev"
    echo "3. Test: cd fastapi-backend && python test_auth.py"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Run the setup script to fix issues:"
    echo "  ./scripts/setup_auth.sh"
    exit 1
fi
