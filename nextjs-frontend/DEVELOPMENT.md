# Development Guide

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Project Structure

```
nextjs-frontend/
├── app/                    # Next.js 15 App Router pages
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── regional/          # Regional analysis feature
│   └── providers.tsx      # React Query provider
├── components/            # Reusable components
│   ├── layout/           # Layout components (Header, Footer)
│   ├── filters/          # Filter components
│   ├── charts/           # Chart components (Recharts)
│   └── stats/            # Statistics components
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions and configurations
├── types/                # TypeScript type definitions
└── public/               # Static assets
```

## Technology Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Charts**: Recharts
- **HTTP Client**: Axios

## Environment Variables

Create `.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development Workflow

### Creating a New Feature Page

1. **Create types** in `types/` directory
2. **Create mock data** in `lib/mock-data.ts`
3. **Create custom hook** in `hooks/`
4. **Create components** in `components/`
5. **Create page** in `app/[feature]/page.tsx`
6. **Add navigation link** in `components/layout/Header.tsx`

### Example: Regional Analysis Feature

```typescript
// 1. Types (types/analysis.ts)
export interface RegionalAnalysis {
  by_region: RegionalDataItem[];
  summary: RegionalSummary;
}

// 2. Mock Data (lib/mock-data.ts)
export const mockRegionalData = { ... };

// 3. Custom Hook (hooks/useRegionalAnalysis.ts)
export function useRegionalAnalysis(filter?: string) {
  return useQuery({ ... });
}

// 4. Components (components/charts/RegionalBarChart.tsx)
export default function RegionalBarChart({ data }) { ... }

// 5. Page (app/regional/page.tsx)
export default function RegionalPage() { ... }
```

## Coding Standards

### Immutability
Always create new objects, never mutate:

```typescript
// ❌ Wrong
function updateData(data: Data) {
  data.value = newValue;
  return data;
}

// ✅ Correct
function updateData(data: Data) {
  return { ...data, value: newValue };
}
```

### No Console Logs
Remove all console.log statements before committing

### TypeScript
- Use strict mode
- Define proper types for all props
- Avoid `any` type

### Component Structure
```typescript
'use client'; // If needed

import { ... } from '...';

interface ComponentProps {
  // Props definition
}

export default function Component({ ... }: ComponentProps) {
  // Component logic
  return (
    // JSX
  );
}
```

## API Integration

### Using Mock Data (Development)
```typescript
// hooks/useRegionalAnalysis.ts
const USE_MOCK_DATA = true; // Development mode
```

### Using Real API (Production)
```typescript
// hooks/useRegionalAnalysis.ts
const USE_MOCK_DATA = false; // Production mode
```

Backend API should be running at `http://localhost:8000`

## Styling Guidelines

### Tailwind CSS Classes
- Use utility classes for styling
- Dark mode: `dark:` prefix
- Responsive: `sm:`, `md:`, `lg:`, `xl:` prefixes

### Color Scheme
- Primary: `blue-500` (#3b82f6)
- Success: `green-500` (#10b981)
- Warning: `amber-500` (#f59e0b)
- Danger: `red-500` (#ef4444)
- Gray scale: `gray-50` to `gray-900`

### Korean Number Formatting
```typescript
// Display in 억원 (hundred millions)
const formatted = Math.round(price / 10000).toLocaleString('ko-KR');
// Example: 150000 -> "15,000만원" or "1.5억원"
```

## Testing

### Component Testing (Future)
```bash
npm test
```

### Type Checking
```bash
npx tsc --noEmit
```

### Linting
```bash
npm run lint
```

## Performance Optimization

### TanStack Query
- Set appropriate `staleTime` (default: 5 minutes)
- Use `queryKey` for proper caching
- Enable automatic refetching when needed

### Chart Performance
- Use `ResponsiveContainer` for responsive charts
- Limit data points for better performance
- Debounce filter changes if needed

## Troubleshooting

### Common Issues

1. **"use client" directive missing**
   - Add `'use client';` at the top of components using hooks

2. **Module not found**
   - Check `@/` path alias in `tsconfig.json`
   - Ensure file exists in correct directory

3. **Hydration errors**
   - Check for client/server rendering mismatches
   - Use `useEffect` for client-only code

4. **API connection failed**
   - Verify backend server is running
   - Check `NEXT_PUBLIC_API_URL` environment variable
   - Enable mock data mode for development

## Next Features to Implement

1. Time-based analysis page
2. Transaction type analysis page
3. Price trend prediction
4. User favorites/bookmarks
5. Export to CSV/Excel
6. Advanced filtering options
7. Comparison mode (multi-region, multi-period)
