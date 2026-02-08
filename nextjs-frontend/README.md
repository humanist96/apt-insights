# Next.js Frontend - 아파트 실거래가 분석 플랫폼

Next.js 15 기반의 한국 아파트 실거래가 데이터 분석 및 시각화 플랫폼 프론트엔드입니다.

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Charts**: Recharts
- **HTTP Client**: Axios

## Getting Started

### Install Dependencies

```bash
npm install
```

### Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm run start
```

## Project Structure

```
nextjs-frontend/
├── app/
│   ├── layout.tsx          # Root layout with Korean fonts
│   ├── page.tsx            # Home page (dashboard)
│   ├── providers.tsx       # TanStack Query provider
│   └── globals.css         # Global styles
├── components/
│   ├── layout/
│   │   ├── Header.tsx      # Top navigation
│   │   ├── Footer.tsx      # Footer
│   │   └── Sidebar.tsx     # Side navigation
│   └── ui/
│       ├── Button.tsx      # Reusable button component
│       └── Card.tsx        # Card component
├── lib/
│   └── api-client.ts       # Axios API client setup
└── public/                 # Static assets
```

## Features

- Korean font support (Noto Sans KR)
- Dark mode support
- Responsive design
- Type-safe API client
- Optimized data fetching with React Query
- Reusable UI components

## API Integration

The frontend connects to the Python backend API (default: `http://localhost:8000`).

Available API endpoints:
- `/api/silv-trade` - 분양권전매 (Pre-sale Rights)
- `/api/apt-trade` - 아파트매매 (Apartment Trade)
- `/api/apt-trade-dev` - 매매상세 (Detailed Trade)
- `/api/apt-rent` - 전월세 (Rental)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## License

This project is part of the apartment real estate analysis platform.
