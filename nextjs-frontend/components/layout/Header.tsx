'use client';

import Link from "next/link";
import UsageIndicator from "@/components/premium/UsageIndicator";

export default function Header() {
  return (
    <header className="border-b bg-white dark:bg-gray-900">
      <nav className="container mx-auto flex items-center justify-between px-4 py-4">
        <Link href="/" className="text-xl font-bold text-gray-900 dark:text-white">
          아파트 실거래가 분석
        </Link>

        <div className="flex items-center gap-6">
          <div className="flex gap-6">
          <Link
            href="/regional"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            지역별 분석
          </Link>
          <Link
            href="/price-trend"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            가격 추이 분석
          </Link>
          <Link
            href="/by-apartment"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            아파트별 분석
          </Link>
          <Link
            href="/price-per-area"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            평당가 분석
          </Link>
          <Link
            href="/bargain-sales"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            급매물 탐지
          </Link>
          <Link
            href="/silv-trade"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            분양권전매
          </Link>
          <Link
            href="/apt-trade"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            아파트매매
          </Link>
          <Link
            href="/apt-trade-dev"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            매매상세
          </Link>
          <Link
            href="/apt-rent"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            전월세
          </Link>
          <Link
            href="/rent-vs-jeonse"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            월세/전세 분석
          </Link>
          <Link
            href="/event-analysis"
            className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            시기 이벤트 분석
          </Link>
          </div>

          <UsageIndicator />
        </div>
      </nav>
    </header>
  );
}
