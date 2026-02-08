#!/bin/bash
# =============================================================================
# Docker Production Deployment Script
# =============================================================================
# This script deploys the application using Docker Compose in production mode

set -e  # Exit on error

echo "========================================"
echo "  Apartment Insights - Production Deploy"
echo "========================================"
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ Error: .env.production file not found!"
    echo ""
    echo "Please create .env.production file:"
    echo "  cp .env.production.example .env.production"
    echo "  nano .env.production"
    echo ""
    exit 1
fi

# Confirm deployment
echo "⚠️  This will deploy the application in PRODUCTION mode."
read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "Step 1/5: Pulling latest images..."
docker-compose -f docker-compose.prod.yml --env-file .env.production pull

echo ""
echo "Step 2/5: Building images..."
docker-compose -f docker-compose.prod.yml --env-file .env.production build --no-cache

echo ""
echo "Step 3/5: Starting services..."
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

echo ""
echo "Step 4/5: Waiting for services to be healthy..."
sleep 10

# Check health
echo ""
echo "Step 5/5: Checking health..."
docker-compose -f docker-compose.prod.yml --env-file .env.production ps

echo ""
echo "Backend health check:"
curl -s http://localhost:8000/health | jq . || echo "❌ Backend not responding"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Access points:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""
echo "View logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "Stop services:"
echo "  docker-compose -f docker-compose.prod.yml down"
