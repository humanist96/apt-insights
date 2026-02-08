#!/bin/bash
# Setup script for monitoring and observability

set -e

echo "========================================"
echo "  Monitoring Setup Script"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from project root
if [ ! -f "MONITORING_OBSERVABILITY.md" ]; then
    echo -e "${RED}Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Step 1: Check dependencies
echo "Step 1: Checking dependencies..."
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python is installed${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Warning: Node.js is not installed (required for frontend)${NC}"
else
    echo -e "${GREEN}✓ Node.js is installed${NC}"
fi

echo ""

# Step 2: Install Python dependencies
echo "Step 2: Installing Python dependencies..."
cd fastapi-backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"
cd ..
echo ""

# Step 3: Install Node.js dependencies (if Node.js is available)
if command -v node &> /dev/null; then
    echo "Step 3: Installing Node.js dependencies..."
    cd nextjs-frontend
    npm install --silent
    echo -e "${GREEN}✓ Node.js dependencies installed${NC}"
    cd ..
    echo ""
else
    echo "Step 3: Skipping Node.js dependencies (Node.js not installed)"
    echo ""
fi

# Step 4: Create environment files
echo "Step 4: Setting up environment files..."

# Backend .env
if [ ! -f "fastapi-backend/.env" ]; then
    cp fastapi-backend/.env.monitoring.example fastapi-backend/.env
    echo -e "${YELLOW}Created fastapi-backend/.env from example${NC}"
    echo -e "${YELLOW}Please edit this file and add your SENTRY_DSN${NC}"
else
    echo -e "${GREEN}fastapi-backend/.env already exists${NC}"
fi

# Frontend .env.local
if [ ! -f "nextjs-frontend/.env.local" ]; then
    cp nextjs-frontend/.env.monitoring.example nextjs-frontend/.env.local
    echo -e "${YELLOW}Created nextjs-frontend/.env.local from example${NC}"
    echo -e "${YELLOW}Please edit this file and add your SENTRY_DSN${NC}"
else
    echo -e "${GREEN}nextjs-frontend/.env.local already exists${NC}"
fi

echo ""

# Step 5: Create log directory
echo "Step 5: Creating log directory..."
mkdir -p fastapi-backend/logs
echo -e "${GREEN}✓ Log directory created${NC}"
echo ""

# Step 6: Start monitoring stack
echo "Step 6: Starting monitoring stack..."
read -p "Do you want to start the monitoring stack (Prometheus, Grafana, Alertmanager)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd monitoring
    docker-compose -f docker-compose.monitoring.yml up -d
    echo -e "${GREEN}✓ Monitoring stack started${NC}"
    echo ""
    echo "Services:"
    echo "  - Prometheus:  http://localhost:9090"
    echo "  - Grafana:     http://localhost:3001 (admin/admin)"
    echo "  - Alertmanager: http://localhost:9093"
    cd ..
else
    echo "Skipped monitoring stack startup"
fi
echo ""

# Step 7: Verify setup
echo "Step 7: Verification..."
echo ""

# Check if Sentry DSN is configured
if grep -q "your-sentry-dsn" fastapi-backend/.env 2>/dev/null; then
    echo -e "${YELLOW}⚠ Warning: Sentry DSN not configured in fastapi-backend/.env${NC}"
    echo "  Please edit the file and add your Sentry DSN"
else
    echo -e "${GREEN}✓ Sentry DSN appears to be configured${NC}"
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Sentry:"
echo "   - Create account at https://sentry.io"
echo "   - Create projects for backend and frontend"
echo "   - Add DSNs to .env files"
echo ""
echo "2. Start the application:"
echo "   Backend:"
echo "     cd fastapi-backend"
echo "     source venv/bin/activate"
echo "     uvicorn main:app --reload"
echo ""
echo "   Frontend:"
echo "     cd nextjs-frontend"
echo "     npm run dev"
echo ""
echo "3. Access monitoring:"
echo "   - Health: http://localhost:8000/api/health/detailed"
echo "   - Metrics: http://localhost:8000/api/metrics"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3001"
echo ""
echo "4. Import Grafana dashboard:"
echo "   - Login to Grafana (admin/admin)"
echo "   - Go to Dashboards → Import"
echo "   - Upload monitoring/grafana-dashboard.json"
echo ""
echo "For detailed documentation, see:"
echo "  - MONITORING_OBSERVABILITY.md"
echo "  - monitoring/README.md"
echo ""
