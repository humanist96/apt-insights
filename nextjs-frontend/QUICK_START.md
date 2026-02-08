# Quick Start - Regional Analysis Feature

## Immediate Testing (Mock Data)

```bash
# 1. Navigate to project
cd /Users/koscom/Downloads/apt_test/nextjs-frontend

# 2. Install dependencies (if not already done)
npm install

# 3. Start development server
npm run dev
```

**Open in browser**: http://localhost:3000/regional

## What You'll See

### Page Layout
```
┌─────────────────────────────────────────────┐
│ Header: 아파트 실거래가 분석               │
│ Nav: [지역별 분석] [분양권전매] ...        │
├─────────────────────────────────────────────┤
│                                             │
│ 지역별 분석                                │
│ 지역별 아파트 거래 현황을 분석합니다       │
│                                             │
│ [지역 선택: 전체 지역 ▼]                   │
│                                             │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│ │총 거래 │ │평균 가격│ │최고가  │ │최저가  ││
│ │7,011건 │ │12,850억│ │15,000억│ │9,500억 ││
│ └────────┘ └────────┘ └────────┘ └────────┘│
│                                             │
│ ┌─────────────────┐ ┌─────────────────┐   │
│ │ Bar Chart       │ │ Pie Chart       │   │
│ │ 지역별 가격/건수│ │ 지역별 거래 비중│   │
│ └─────────────────┘ └─────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### Interactive Features

1. **Region Filter**
   - Click dropdown to select region
   - Options: 전체 지역, 강남구, 서초구, etc.
   - Data updates automatically on selection

2. **Stats Cards**
   - Hover for shadow effect
   - Numbers formatted in Korean locale
   - Prices displayed in 억원

3. **Charts**
   - Bar Chart: Hover over bars for tooltips
   - Pie Chart: Hover over slices for details
   - Responsive to window resize

## Testing Checklist

### Visual Tests
- [ ] Page loads without errors
- [ ] All 4 stats cards display correctly
- [ ] Bar chart renders with proper axes
- [ ] Pie chart shows all regions
- [ ] Korean text displays properly
- [ ] Numbers use Korean formatting (15,000억원)
- [ ] Dark mode works (if enabled)

### Interaction Tests
- [ ] Region filter dropdown opens
- [ ] Selecting region updates data
- [ ] Selecting "전체 지역" shows all data
- [ ] Charts update when filter changes
- [ ] Tooltips appear on chart hover
- [ ] Loading skeleton shows briefly (500ms)

### Responsive Tests
- [ ] Mobile view (< 640px): Single column
- [ ] Tablet view (640-1024px): Flexible grid
- [ ] Desktop view (> 1024px): Multi-column layout
- [ ] Charts resize smoothly

### Data Verification
```javascript
// Expected mock data totals:
Total Transactions: 7,011
Average Price: 12,850억원
Highest: 강남구 (15,000억원)
Lowest: 영등포구 (9,500억원)

// Region breakdown:
강남구: 1,234건, 15,000억원
서초구: 987건, 14,000억원
송파구: 1,456건, 12,500억원
마포구: 765건, 11,000억원
용산구: 543건, 14,500억원
영등포구: 892건, 9,500억원
양천구: 678건, 10,500억원
광진구: 456건, 9,800억원
```

## Switching to Real API

### Step 1: Update Hook
```typescript
// File: hooks/useRegionalAnalysis.ts
// Line 6: Change from true to false
const USE_MOCK_DATA = false; // Production mode
```

### Step 2: Start Backend
```bash
# In separate terminal
cd /Users/koscom/Downloads/apt_test
# Start your FastAPI backend
python -m uvicorn main:app --reload --port 8000
```

### Step 3: Verify Environment
```bash
# Create .env.local if not exists
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### Step 4: Restart Next.js
```bash
# Stop dev server (Ctrl+C)
npm run dev
```

## Troubleshooting

### Issue: Page shows blank
**Solution**: Check browser console for errors
```bash
# Open browser DevTools (F12)
# Look for error messages
```

### Issue: Charts not rendering
**Solution**: Verify Recharts is installed
```bash
npm list recharts
# Should show: recharts@2.15.0
```

### Issue: Korean text appears broken
**Solution**: Check font loading
- Inspect page source
- Verify Noto Sans KR font loads
- Check network tab for font files

### Issue: API connection fails
**Solution**: Verify backend is running
```bash
curl http://localhost:8000/api/v1/health
# Should return: {"status":"healthy"}
```

### Issue: Stale data not updating
**Solution**: Clear React Query cache
- Refresh page (F5)
- Or clear browser cache
- Or reduce staleTime in hook

## Development Tips

### Hot Reload
Next.js auto-reloads on file changes. Edit any file and save to see changes instantly.

### TypeScript Errors
```bash
# Check for type errors
npx tsc --noEmit
```

### Inspect React Query
Install React Query DevTools for debugging:
```typescript
// Add to app/providers.tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

<ReactQueryDevtools initialIsOpen={false} />
```

### Mock Different Scenarios

#### Filter by Region
```typescript
// In browser console:
localStorage.setItem('selectedRegion', '강남구')
location.reload()
```

#### Simulate Loading
```typescript
// Increase delay in hooks/useRegionalAnalysis.ts
await new Promise((resolve) => setTimeout(resolve, 3000)); // 3 seconds
```

#### Simulate Error
```typescript
// In hooks/useRegionalAnalysis.ts
if (USE_MOCK_DATA) {
  throw new Error('Test error message');
}
```

## Performance Monitoring

### Check Render Performance
```javascript
// Browser DevTools → Performance
// Record while interacting with page
// Look for:
// - Layout shifts (should be minimal)
// - Paint times (should be < 16ms)
// - JS execution (should be optimized)
```

### Check Bundle Size
```bash
npm run build
# Look for .next/static output
# Verify page size is reasonable
```

## Next Actions

1. ✅ Verify page loads correctly
2. ✅ Test all interactive features
3. ✅ Check responsive design
4. ⏳ Connect to real backend API
5. ⏳ Test with production data
6. ⏳ Deploy to staging environment

## Support

- **Feature Documentation**: `app/regional/README.md`
- **Development Guide**: `DEVELOPMENT.md`
- **Implementation Summary**: `FEATURE_SUMMARY.md`
- **Project Overview**: `CLAUDE.md`

## Success Metrics

When testing is successful:
- [ ] Page loads in < 2 seconds
- [ ] All interactions work smoothly
- [ ] No console errors
- [ ] No TypeScript errors
- [ ] Responsive on all screen sizes
- [ ] Korean text displays correctly
- [ ] Charts render properly
- [ ] Data updates on filter change

**Status**: Ready for testing ✅
