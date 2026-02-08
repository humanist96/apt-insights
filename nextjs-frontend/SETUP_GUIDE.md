# Next.js Frontend Setup Guide

## Installation Steps

### 1. Install Dependencies

Run the installation script:

```bash
cd /Users/koscom/Downloads/apt_test/nextjs-frontend
chmod +x INSTALL.sh
./INSTALL.sh
```

Or manually install:

```bash
cd /Users/koscom/Downloads/apt_test/nextjs-frontend
npm install
```

### 2. Verify Environment Configuration

Check that `.env.local` exists with the correct API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at: http://localhost:3000

## Project Structure Overview

```
nextjs-frontend/
├── app/                         # Next.js App Router
│   ├── layout.tsx              # Root layout with Korean fonts (Noto Sans KR)
│   ├── page.tsx                # Home page - Dashboard intro
│   ├── providers.tsx           # TanStack Query provider setup
│   └── globals.css             # Tailwind CSS + custom styles
│
├── components/
│   ├── layout/
│   │   ├── Header.tsx          # Top navigation bar
│   │   ├── Footer.tsx          # Footer with links
│   │   └── Sidebar.tsx         # Optional side navigation
│   └── ui/
│       ├── Button.tsx          # Reusable button component
│       └── Card.tsx            # Card component for sections
│
├── lib/
│   └── api-client.ts           # Axios API client configuration
│
├── public/                      # Static assets
│
├── .env.local                   # Environment variables
├── package.json                 # Dependencies
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.ts          # Tailwind CSS configuration
└── next.config.ts              # Next.js configuration
```

## Key Technologies

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **TanStack Query**: Data fetching and caching
- **Zustand**: State management (ready to use)
- **Recharts**: Charting library (ready to use)
- **Axios**: HTTP client with interceptors

## Korean Font Support

The project uses **Noto Sans KR** from Google Fonts, configured in `app/layout.tsx`:

```typescript
const notoSansKr = Noto_Sans_KR({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-noto-sans-kr",
  display: "swap",
});
```

## Component Examples

### Using Button Component

```typescript
import Button from "@/components/ui/Button";

<Button variant="primary" onClick={handleClick}>
  클릭하세요
</Button>

<Button variant="secondary">취소</Button>
<Button variant="outline">외곽선</Button>
```

### Using Card Component

```typescript
import Card from "@/components/ui/Card";

<Card
  title="제목"
  description="설명"
>
  <p>카드 내용</p>
</Card>
```

### Using API Client

```typescript
import { apiClient } from "@/lib/api-client";

const response = await apiClient.get('/api/apt-trade', {
  params: { region: '11680', date: '202312' }
});
```

## TanStack Query Usage

The project is configured with TanStack Query for data fetching:

```typescript
'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export function useAptTradeData(region: string, date: string) {
  return useQuery({
    queryKey: ['apt-trade', region, date],
    queryFn: async () => {
      const { data } = await apiClient.get('/api/apt-trade', {
        params: { region, date }
      });
      return data;
    },
  });
}
```

## Available Scripts

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Next Steps

1. **Install dependencies** (run INSTALL.sh)
2. **Verify the backend API is running** (http://localhost:8000)
3. **Start the development server** (`npm run dev`)
4. **Create feature pages** in the `app/` directory
5. **Build data fetching hooks** using TanStack Query
6. **Add chart components** using Recharts

## Success Criteria Checklist

- [x] Next.js project initialized with TypeScript
- [x] Tailwind CSS configured
- [x] Korean fonts (Noto Sans KR) configured
- [x] Basic layout components created (Header, Footer, Sidebar)
- [x] Reusable UI components created (Button, Card)
- [x] API client setup with Axios
- [x] TanStack Query provider configured
- [x] Environment variables configured
- [x] ESLint configured
- [x] Git ignore file created
- [ ] Dependencies installed (run `npm install`)
- [ ] Development server tested (run `npm run dev`)

## Troubleshooting

### Port 3000 already in use

```bash
# Find process using port 3000
lsof -ti:3000

# Kill the process
kill -9 <PID>

# Or use a different port
npm run dev -- -p 3001
```

### Module not found errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript errors

```bash
# Check TypeScript configuration
npx tsc --noEmit
```

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Recharts Documentation](https://recharts.org/)
