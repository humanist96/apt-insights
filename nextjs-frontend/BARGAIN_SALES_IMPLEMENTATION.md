# Bargain Sales Detection Implementation

## Overview
Implemented the bargain sales detection page (급매물 탐지) in Next.js frontend, following the Streamlit reference implementation.

## Files Created

### 1. Types (`types/analysis.ts`)
Added new interfaces:
- `BargainSalesItem` - Individual bargain sale item with discount info
- `BargainSalesRegion` - Regional bargain statistics
- `BargainSalesAnalysis` - Complete analysis response

### 2. Hook (`hooks/useBargainSales.ts`)
- Custom TanStack Query hook for bargain sales data
- Parameters: `regionFilter`, `thresholdPct`, `minTransactionCount`
- Implements filtering and dynamic threshold adjustment
- 5-minute cache for performance
- Mock data mode enabled (USE_MOCK_DATA = true)

### 3. Mock Data (`lib/mock-data.ts`)
Added `mockBargainSales` with:
- 25 realistic bargain opportunities across Seoul regions
- Discount range: 10-25%
- Total savings: 66.5억원
- Regional distribution matching actual patterns

### 4. Charts

#### BargainSalesScatter (`components/charts/BargainSalesScatter.tsx`)
- Scatter plot: X-axis (expected price) vs Y-axis (actual price)
- Bubble size represents discount percentage
- Color-coded by discount level:
  - Red: 초특급 (≥25%)
  - Orange: 특급 (20-25%)
  - Amber: 일반 (15-20%)
  - Green: 경미 (<15%)
- Diagonal reference line showing "no discount" baseline
- Interactive tooltips with apartment details

#### BargainDistributionChart (`components/charts/BargainDistributionChart.tsx`)
- Bar chart showing bargain count by region
- Top 10 regions displayed
- Color-coded by bargain rate
- Rotated labels for readability

### 5. Table (`components/BargainSalesTable.tsx`)
- Sortable columns: discount %, savings, price, date
- Badge indicators for discount levels
- Responsive design with dark mode support
- Korean number formatting (억원, 만원)

### 6. Main Page (`app/bargain-sales/page.tsx`)
Features:
- Region filter
- Discount threshold slider (10-30%, default 15%)
- Min transaction count filter (2-10 deals)
- Summary metrics cards:
  - 급매물 수 (bargain count)
  - 평균 할인율 (average discount)
  - 최대 할인율 (max discount)
  - 총 절감액 (total savings)
- Discount level breakdown (초특급/특급/일반/경미)
- Regional distribution chart
- Scatter plot visualization
- Detailed sortable table
- Loading skeleton
- Error handling
- Empty state messaging

### 7. Navigation (`components/layout/Header.tsx`)
Added "급매물 탐지" link to navigation menu

## Key Features

### Discount Detection Logic
- Compares transaction price with average of recent 5 deals
- Same apartment + similar area (±5㎡ grouping)
- Configurable threshold percentage
- Realistic savings calculation

### User Controls
1. **Region Filter**: Filter by specific Seoul district
2. **Threshold Slider**: Adjust discount sensitivity (10-30%)
3. **Min Deals Filter**: Require minimum transaction history

### Visualizations
1. **Summary Cards**: Key metrics at a glance
2. **Level Breakdown**: Distribution by discount severity
3. **Regional Chart**: Geographic distribution of bargains
4. **Scatter Plot**: Price comparison visualization
5. **Data Table**: Detailed sortable list

## Testing

### Build Status
```bash
✓ Compiled successfully
✓ Generating static pages (13/13)
Route: /bargain-sales - 5.68 kB - 249 kB First Load
```

### Dev Server
```bash
npm run dev
# Access: http://localhost:3001/bargain-sales
```

## Design Patterns

### Immutability
All data transformations use spread operators and non-mutating methods:
```typescript
const sortedData = [...data].sort(...)
const filteredItems = mockBargainSales.data.bargain_items.filter(...)
```

### TypeScript Strict Mode
- Full type safety with no `any` types (except Recharts props)
- Interface-driven development
- Proper error handling

### Responsive Design
- Mobile-first approach
- Grid layouts with breakpoints
- Horizontal scroll for tables
- Touch-friendly controls

### Korean Formatting
- 억원 (hundred million won)
- 만원 (ten thousand won)
- % (percentage)
- ㎡ (square meters)
- 건 (count)

### Dark Mode Support
All components support dark mode with proper color schemes

## Mock Data Statistics
- Total items: 25 bargain opportunities
- Regions covered: 12 Seoul districts
- Price range: 6.3억 - 50억원
- Discount range: 10.0% - 25.0%
- Average discount: 15.6%
- Total savings: 66.5억원

## API Integration (Ready)
When backend is ready, change in `hooks/useBargainSales.ts`:
```typescript
const USE_MOCK_DATA = false; // Enable real API
```

Expected endpoint:
```
POST /api/v1/investment/bargain-sales
Body: {
  region_filter?: string,
  threshold_pct?: number,
  min_transaction_count?: number,
  start_date?: string,
  end_date?: string
}
```

## Future Enhancements
1. Add date range filter
2. Export bargain list to CSV/Excel
3. Set price alerts for specific apartments
4. Historical bargain trend analysis
5. Email notifications for new bargains
6. Favorite/watchlist functionality

## References
- Streamlit implementation: `/frontend/app.py` lines 2760-2850
- Python analyzer: `/backend/analyzer.py` lines 1173-1323
