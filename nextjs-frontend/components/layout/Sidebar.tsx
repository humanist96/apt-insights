'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  { href: "/", label: "대시보드" },
  { href: "/regional", label: "지역별 분석" },
  { href: "/by-apartment", label: "아파트별 분석" },
  { href: "/price-trend", label: "가격 추이" },
  { href: "/investment", label: "갭투자 분석" },
  { href: "/detail-data", label: "상세 데이터" },
  { href: "/silv-trade", label: "분양권전매" },
  { href: "/apt-trade", label: "아파트매매" },
  { href: "/apt-trade-dev", label: "매매상세" },
  { href: "/apt-rent", label: "전월세" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-white dark:bg-gray-900">
      <nav className="space-y-1 p-4">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-50 text-blue-700 dark:bg-blue-900 dark:text-blue-200"
                  : "text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-800"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
