#!/bin/bash

# Regional Analysis Feature Validation Script
# Run this to verify all files are present and properly structured

echo "🔍 Validating Regional Analysis Feature..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for checks
PASSED=0
FAILED=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $1 (MISSING)"
        ((FAILED++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (MISSING)"
        ((FAILED++))
        return 1
    fi
}

echo "📁 Checking Directory Structure..."
echo "──────────────────────────────────"
check_dir "app/regional"
check_dir "components/stats"
check_dir "components/filters"
check_dir "components/charts"
check_dir "hooks"
check_dir "types"
check_dir "lib"
echo ""

echo "📄 Checking Type Definitions..."
echo "──────────────────────────────────"
check_file "types/analysis.ts"
echo ""

echo "📄 Checking Mock Data..."
echo "──────────────────────────────────"
check_file "lib/mock-data.ts"
echo ""

echo "📄 Checking Custom Hooks..."
echo "──────────────────────────────────"
check_file "hooks/useRegionalAnalysis.ts"
echo ""

echo "📄 Checking Components..."
echo "──────────────────────────────────"
check_file "components/stats/StatsCard.tsx"
check_file "components/filters/RegionFilter.tsx"
check_file "components/charts/RegionalBarChart.tsx"
check_file "components/charts/RegionalPieChart.tsx"
echo ""

echo "📄 Checking Pages..."
echo "──────────────────────────────────"
check_file "app/regional/page.tsx"
echo ""

echo "📄 Checking Updated Files..."
echo "──────────────────────────────────"
check_file "components/layout/Header.tsx"
check_file "lib/api-client.ts"
echo ""

echo "📄 Checking Documentation..."
echo "──────────────────────────────────"
check_file "app/regional/README.md"
check_file "DEVELOPMENT.md"
check_file "FEATURE_SUMMARY.md"
check_file "QUICK_START.md"
echo ""

echo "🔧 Checking Dependencies..."
echo "──────────────────────────────────"

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules/ (dependencies installed)"
    ((PASSED++))

    # Check specific packages
    if [ -d "node_modules/@tanstack/react-query" ]; then
        echo -e "${GREEN}✓${NC} @tanstack/react-query installed"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} @tanstack/react-query (MISSING - run npm install)"
        ((FAILED++))
    fi

    if [ -d "node_modules/recharts" ]; then
        echo -e "${GREEN}✓${NC} recharts installed"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} recharts (MISSING - run npm install)"
        ((FAILED++))
    fi

    if [ -d "node_modules/axios" ]; then
        echo -e "${GREEN}✓${NC} axios installed"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} axios (MISSING - run npm install)"
        ((FAILED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} node_modules/ not found - run 'npm install'"
    echo -e "${YELLOW}⚠${NC} Skipping dependency checks"
fi
echo ""

echo "📊 TypeScript Validation..."
echo "──────────────────────────────────"
if command -v npx &> /dev/null; then
    echo "Running TypeScript type check..."
    if npx tsc --noEmit 2>&1 | grep -q "error TS"; then
        echo -e "${RED}✗${NC} TypeScript errors found"
        echo "Run 'npx tsc --noEmit' to see details"
        ((FAILED++))
    else
        echo -e "${GREEN}✓${NC} No TypeScript errors"
        ((PASSED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} npx not found - skipping TypeScript check"
fi
echo ""

echo "════════════════════════════════════════"
echo "Summary"
echo "════════════════════════════════════════"
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run 'npm run dev' to start development server"
    echo "2. Open http://localhost:3000/regional in browser"
    echo "3. Test the feature with mock data"
    echo "4. See QUICK_START.md for testing guide"
    exit 0
else
    echo -e "${RED}❌ Some checks failed${NC}"
    echo ""
    echo "Please fix the issues above before proceeding."
    exit 1
fi
