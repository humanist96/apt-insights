#!/bin/bash

# Installation script for Next.js frontend
# Run this script to install all dependencies

echo "Installing Next.js dependencies..."
cd "$(dirname "$0")"
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Installation complete!"
    echo ""
    echo "To start the development server, run:"
    echo "  cd nextjs-frontend"
    echo "  npm run dev"
    echo ""
    echo "The app will be available at http://localhost:3000"
else
    echo ""
    echo "✗ Installation failed. Please check the error messages above."
    exit 1
fi
