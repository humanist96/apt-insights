#!/bin/bash
# Startup script for FastAPI backend

echo "========================================"
echo "FastAPI Backend - Apartment Analysis"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found"
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Check if backend exists
if [ ! -d "../backend" ]; then
    echo "❌ Backend directory not found"
    echo "   Make sure you're running this from fastapi-backend/"
    exit 1
fi

echo ""
echo "🚀 Starting FastAPI server..."
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo "   Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start server
python main.py
