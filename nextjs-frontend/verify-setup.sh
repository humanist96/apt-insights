#!/bin/bash

echo "=== Next.js Frontend Setup Verification ==="
echo ""

cd "$(dirname "$0")"

# Check required files
echo "Checking required files..."
files=(
    "package.json"
    "tsconfig.json"
    "next.config.ts"
    "tailwind.config.ts"
    ".env.local"
    "app/layout.tsx"
    "app/page.tsx"
    "app/providers.tsx"
    "components/layout/Header.tsx"
    "components/layout/Footer.tsx"
    "components/ui/Button.tsx"
    "components/ui/Card.tsx"
    "lib/api-client.ts"
)

missing_files=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (MISSING)"
        missing_files=$((missing_files + 1))
    fi
done

echo ""

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "✓ node_modules directory exists (dependencies installed)"
else
    echo "✗ node_modules directory not found"
    echo "  Run: npm install"
fi

echo ""

# Check package.json dependencies
echo "Checking package.json dependencies..."
required_deps=(
    "next"
    "react"
    "react-dom"
    "@tanstack/react-query"
    "recharts"
    "zustand"
    "axios"
    "typescript"
    "tailwindcss"
)

for dep in "${required_deps[@]}"; do
    if grep -q "\"$dep\"" package.json; then
        echo "✓ $dep"
    else
        echo "✗ $dep (MISSING)"
    fi
done

echo ""
echo "=== Summary ==="
if [ $missing_files -eq 0 ]; then
    echo "✓ All required files are present"
else
    echo "✗ $missing_files file(s) missing"
fi

if [ -d "node_modules" ]; then
    echo "✓ Dependencies installed"
    echo ""
    echo "Ready to run: npm run dev"
else
    echo "⚠ Dependencies not installed yet"
    echo ""
    echo "Next steps:"
    echo "  1. Run: npm install"
    echo "  2. Run: npm run dev"
    echo "  3. Open: http://localhost:3000"
fi
