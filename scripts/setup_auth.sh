#!/bin/bash

# Authentication Setup Script
# This script sets up the authentication system for the apartment analysis platform

set -e

echo "==========================================="
echo "Authentication System Setup"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if PostgreSQL is running
echo "1. Checking PostgreSQL..."
if pg_isready -q; then
    print_success "PostgreSQL is running"
else
    print_error "PostgreSQL is not running"
    echo "  Please start PostgreSQL before continuing"
    exit 1
fi

# Generate JWT secret if not exists
echo ""
echo "2. Checking JWT secret key..."
if grep -q "JWT_SECRET_KEY=your-secret-key" fastapi-backend/.env 2>/dev/null || [ ! -f fastapi-backend/.env ]; then
    print_warning "Generating new JWT secret key..."
    JWT_SECRET=$(openssl rand -hex 32)

    # Create or update .env file
    if [ -f fastapi-backend/.env ]; then
        # Update existing file
        if grep -q "JWT_SECRET_KEY=" fastapi-backend/.env; then
            sed -i.bak "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET/" fastapi-backend/.env
        else
            echo "JWT_SECRET_KEY=$JWT_SECRET" >> fastapi-backend/.env
        fi
    else
        # Create new .env from example
        cp fastapi-backend/.env.example fastapi-backend/.env
        sed -i.bak "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET/" fastapi-backend/.env
    fi

    print_success "JWT secret key generated and saved to fastapi-backend/.env"
else
    print_success "JWT secret key already configured"
fi

# Install Python dependencies
echo ""
echo "3. Installing Python dependencies..."
cd fastapi-backend
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi
cd ..

# Run database migration
echo ""
echo "4. Running database migration..."
echo "  Creating authentication tables..."

# Get database credentials from .env
DB_NAME=$(grep DATABASE_URL .env 2>/dev/null | cut -d '/' -f 4 | cut -d '?' -f 1 || echo "apartment_db")
DB_USER=$(grep DATABASE_URL .env 2>/dev/null | cut -d '@' -f 1 | cut -d '/' -f 3 | cut -d ':' -f 1 || echo "postgres")

# Run migration
if psql -U "$DB_USER" -d "$DB_NAME" -f fastapi-backend/migrations/001_create_auth_tables.sql > /dev/null 2>&1; then
    print_success "Database migration completed"
else
    print_warning "Migration may have already been run (this is OK)"
fi

# Install Node.js dependencies
echo ""
echo "5. Installing Node.js dependencies..."
cd nextjs-frontend
npm install --silent
if [ $? -eq 0 ]; then
    print_success "Node.js dependencies installed"
else
    print_error "Failed to install Node.js dependencies"
    exit 1
fi
cd ..

# Create .env.local if not exists
echo ""
echo "6. Checking Next.js environment..."
if [ ! -f nextjs-frontend/.env.local ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > nextjs-frontend/.env.local
    print_success "Created nextjs-frontend/.env.local"
else
    print_success "Next.js environment already configured"
fi

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the FastAPI backend:"
echo "   cd fastapi-backend"
echo "   uvicorn main:app --reload"
echo ""
echo "2. In another terminal, start the Next.js frontend:"
echo "   cd nextjs-frontend"
echo "   npm run dev"
echo ""
echo "3. Test the authentication:"
echo "   cd fastapi-backend"
echo "   python test_auth.py"
echo ""
echo "4. Visit the application:"
echo "   http://localhost:3000"
echo ""
echo "Available auth pages:"
echo "   - Login: http://localhost:3000/login"
echo "   - Register: http://localhost:3000/register"
echo "   - Profile: http://localhost:3000/profile"
echo ""
print_success "Authentication system is ready!"
