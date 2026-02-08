#!/bin/bash

echo "======================================"
echo "Detail Data Page Verification Script"
echo "======================================"
echo ""

# Check all created files exist
echo "1. Checking Created Files..."
echo "----------------------------"

FILES=(
  "app/detail-data/page.tsx"
  "components/filters/DetailDataFilters.tsx"
  "components/tables/DetailDataTable.tsx"
  "components/ui/ExportButton.tsx"
  "hooks/useDetailData.ts"
)

ALL_EXIST=true
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (MISSING)"
    ALL_EXIST=false
  fi
done

echo ""

# Check type definitions
echo "2. Checking Type Definitions..."
echo "--------------------------------"
if grep -q "DetailDataItem" types/analysis.ts && \
   grep -q "DetailDataFilters" types/analysis.ts && \
   grep -q "DetailDataResponse" types/analysis.ts; then
  echo "✓ Type definitions added to types/analysis.ts"
else
  echo "✗ Type definitions missing"
  ALL_EXIST=false
fi

echo ""

# Check mock data
echo "3. Checking Mock Data..."
echo "------------------------"
if grep -q "generateDetailDataItems" lib/mock-data.ts && \
   grep -q "mockDetailData" lib/mock-data.ts; then
  echo "✓ Mock data functions added to lib/mock-data.ts"
else
  echo "✗ Mock data missing"
  ALL_EXIST=false
fi

echo ""

# Check sidebar menu
echo "4. Checking Navigation..."
echo "-------------------------"
if grep -q "상세 데이터" components/layout/Sidebar.tsx; then
  echo "✓ Sidebar menu item added"
else
  echo "✗ Sidebar menu item missing"
  ALL_EXIST=false
fi

echo ""

# Check build
echo "5. Running Build Test..."
echo "------------------------"
if npm run build > /tmp/build-check.log 2>&1; then
  echo "✓ Build successful"
  # Count pages
  PAGE_COUNT=$(grep -c "○ /" /tmp/build-check.log)
  echo "  Pages built: $PAGE_COUNT"

  # Check if detail-data page is included
  if grep -q "○ /detail-data" /tmp/build-check.log; then
    echo "  ✓ /detail-data page included"
  else
    echo "  ✗ /detail-data page not found in build"
    ALL_EXIST=false
  fi
else
  echo "✗ Build failed (check /tmp/build-check.log)"
  ALL_EXIST=false
fi

echo ""

# Check for code quality issues
echo "6. Code Quality Checks..."
echo "-------------------------"

CONSOLE_LOGS=$(grep -r "console.log" app/detail-data components/filters/DetailDataFilters.tsx components/tables/DetailDataTable.tsx components/ui/ExportButton.tsx hooks/useDetailData.ts 2>/dev/null | wc -l)

if [ "$CONSOLE_LOGS" -eq 0 ]; then
  echo "✓ No console.log statements"
else
  echo "✗ Found $CONSOLE_LOGS console.log statements"
  ALL_EXIST=false
fi

echo ""

# Final result
echo "======================================"
if [ "$ALL_EXIST" = true ]; then
  echo "✓ ALL CHECKS PASSED"
  echo "======================================"
  echo ""
  echo "To test the page:"
  echo "  npm run dev"
  echo "  Open http://localhost:3001/detail-data"
  echo ""
  exit 0
else
  echo "✗ SOME CHECKS FAILED"
  echo "======================================"
  exit 1
fi
