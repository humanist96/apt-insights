# Regional Analysis Page (지역별 분석)

## Overview
Complete implementation of the Regional Analysis feature page for the Korean apartment real estate analysis platform.

## Features Implemented

### 1. Data Fetching
- **Hook**: `hooks/useRegionalAnalysis.ts`
- Uses TanStack Query for efficient data fetching and caching
- Supports filtering by region
- Mock data mode for development (toggle `USE_MOCK_DATA` flag)
- 5-minute stale time for cached data

### 2. UI Components

#### Stats Cards
- Total transactions count
- Average price (displayed in 억원)
- Highest price region
- Lowest price region

#### Charts
- **Bar Chart**: Regional comparison showing average price and transaction count
- **Pie Chart**: Transaction volume distribution by region

#### Filters
- Region dropdown selector
- 8 major Seoul regions + "All regions" option

### 3. Responsive Design
- Mobile: Single column layout
- Desktop: Multi-column grid layout
- Charts adapt to screen size using ResponsiveContainer

### 4. Loading & Error States
- Skeleton loading animation
- Error message display with details
- Empty state for no data

## File Structure

```
app/regional/
  └── page.tsx              # Main page component

components/
  ├── filters/
  │   └── RegionFilter.tsx  # Region selection dropdown
  ├── charts/
  │   ├── RegionalBarChart.tsx  # Bar chart for regional comparison
  │   └── RegionalPieChart.tsx  # Pie chart for distribution
  └── stats/
      └── StatsCard.tsx     # Reusable stats display card

hooks/
  └── useRegionalAnalysis.ts  # Data fetching hook

types/
  └── analysis.ts           # TypeScript type definitions

lib/
  └── mock-data.ts          # Mock data for development
```

## Usage

### Development Mode (Mock Data)
```bash
npm run dev
```
Navigate to http://localhost:3000/regional

The page will use mock data automatically. To switch to real API:
1. Open `hooks/useRegionalAnalysis.ts`
2. Set `USE_MOCK_DATA = false`
3. Ensure backend API is running at http://localhost:8000

### Production Mode (Real API)
1. Set environment variable: `NEXT_PUBLIC_API_URL=http://localhost:8000`
2. Switch `USE_MOCK_DATA` to `false` in the hook
3. Start the backend API server
4. Build and run: `npm run build && npm start`

## API Integration

### Expected API Endpoint
```
POST /api/v1/analysis/regional
Content-Type: application/json

Request Body:
{
  "region_filter": "강남구" // optional, omit for all regions
}

Response:
{
  "success": true,
  "data": {
    "by_region": [
      {
        "region": "강남구",
        "count": 1234,
        "avg_price": 150000,
        "total": 185100000
      }
    ],
    "summary": {
      "total_transactions": 7011,
      "average_price": 128500,
      "total_volume": 868783000,
      "highest_region": {
        "region": "강남구",
        "avg_price": 150000
      },
      "lowest_region": {
        "region": "영등포구",
        "avg_price": 95000
      }
    }
  }
}
```

## Korean Number Formatting
All prices are formatted with Korean locale:
- `toLocaleString('ko-KR')` for number formatting
- Prices displayed in 억원 (hundred millions)
- Division by 10,000 to convert to 억 units

## Supported Regions
- 전체 지역 (All regions)
- 강남구
- 서초구
- 송파구
- 마포구
- 용산구
- 영등포구
- 양천구
- 광진구

## Styling
- Tailwind CSS for all styling
- Dark mode support
- Consistent color scheme:
  - Primary: Blue (#3b82f6)
  - Success: Green (#10b981)
  - Warning: Amber (#f59e0b)
  - Danger: Red (#ef4444)

## Performance
- Client-side rendering with React Server Components support
- Query caching with 5-minute stale time
- Automatic refetch on filter change
- Optimized re-renders with proper memoization

## Next Steps
1. Connect to real backend API
2. Add more regions (expand beyond Seoul)
3. Add date range filtering
4. Export data functionality
5. Add trend analysis over time
6. Implement comparison mode (multi-region)
