# Quick Start Guide

## 3 Steps to Get Running

### Step 1: Install Dependencies
```bash
cd /Users/koscom/Downloads/apt_test/nextjs-frontend
npm install
```

### Step 2: Start Development Server
```bash
npm run dev
```

### Step 3: Open Browser
Navigate to: **http://localhost:3000**

---

## What You'll See

- **Home Page** with 4 feature cards:
  - 분양권전매 (Pre-sale Rights)
  - 아파트매매 (Apartment Trade)
  - 매매상세 (Detailed Trade)
  - 전월세 (Rental)

- **Navigation Header** with links to all sections

- **Footer** with links to 공공데이터포털 and 국토교통부

---

## Project Details

**Framework**: Next.js 15
**Language**: TypeScript
**Styling**: Tailwind CSS
**Font**: Noto Sans KR (Korean)
**API**: http://localhost:8000 (configured in .env.local)

---

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |

---

## File Structure

```
nextjs-frontend/
├── app/                    # Next.js App Router
├── components/             # Reusable components
├── lib/                    # Utilities (API client)
└── public/                 # Static assets
```

---

## Next Steps After Installation

1. ✅ Install dependencies (`npm install`)
2. ✅ Start dev server (`npm run dev`)
3. 📝 Create feature pages in `app/`
4. 📝 Build data fetching hooks
5. 📝 Add chart components with Recharts

---

## Need Help?

- See `SETUP_GUIDE.md` for detailed instructions
- See `PROJECT_STATUS.md` for complete status
- See `README.md` for project overview

---

## Verify Installation

Run the verification script:
```bash
chmod +x verify-setup.sh
./verify-setup.sh
```

This will check that all required files are in place.
