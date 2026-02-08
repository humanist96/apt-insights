'use client';

import Link from "next/link";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Crown,
  BarChart3,
  TrendingUp,
  Building2,
  DollarSign,
  Search,
  Menu,
  X,
  ChevronDown,
  Sparkles
} from "lucide-react";
import UsageIndicator from "@/components/premium/UsageIndicator";

const analysisMenuItems = [
  { href: "/regional", label: "지역별 분석", icon: BarChart3 },
  { href: "/price-trend", label: "가격 추이", icon: TrendingUp },
  { href: "/by-apartment", label: "아파트별", icon: Building2 },
  { href: "/price-per-area", label: "평당가 분석", icon: DollarSign },
];

const dataMenuItems = [
  { href: "/silv-trade", label: "분양권전매" },
  { href: "/apt-trade", label: "아파트매매" },
  { href: "/apt-trade-dev", label: "매매상세" },
  { href: "/apt-rent", label: "전월세" },
];

const advancedMenuItems = [
  { href: "/bargain-sales", label: "급매물 탐지", badge: "HOT" },
  { href: "/rent-vs-jeonse", label: "월세/전세 분석" },
  { href: "/event-analysis", label: "시기 이벤트 분석" },
];

export default function Header() {
  const [isAnalysisOpen, setIsAnalysisOpen] = useState(false);
  const [isDataOpen, setIsDataOpen] = useState(false);
  const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-slate-900/80 backdrop-blur-xl">
      <nav className="container mx-auto flex items-center justify-between px-4 py-4">
        {/* Logo */}
        <Link href="/" className="group flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-r from-blue-600 to-purple-600">
            <Crown className="h-5 w-5 text-white" />
          </div>
          <span className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
            APT Insights
          </span>
          <span className="ml-1 rounded-full bg-gradient-to-r from-amber-500 to-amber-600 px-2 py-0.5 text-xs font-bold text-white">
            PRO
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden items-center gap-8 lg:flex">
          {/* Analysis Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setIsAnalysisOpen(true)}
            onMouseLeave={() => setIsAnalysisOpen(false)}
          >
            <button className="flex items-center gap-1 text-slate-300 transition-colors hover:text-white">
              분석 도구
              <ChevronDown className={`h-4 w-4 transition-transform ${isAnalysisOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {isAnalysisOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.2 }}
                  className="absolute left-0 top-full mt-2 w-64 overflow-hidden rounded-2xl border border-white/10 bg-slate-800/95 backdrop-blur-xl"
                >
                  {analysisMenuItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className="flex items-center gap-3 px-4 py-3 text-slate-300 transition-colors hover:bg-white/5 hover:text-white"
                    >
                      <item.icon className="h-5 w-5" />
                      {item.label}
                    </Link>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Data Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setIsDataOpen(true)}
            onMouseLeave={() => setIsDataOpen(false)}
          >
            <button className="flex items-center gap-1 text-slate-300 transition-colors hover:text-white">
              데이터 조회
              <ChevronDown className={`h-4 w-4 transition-transform ${isDataOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {isDataOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.2 }}
                  className="absolute left-0 top-full mt-2 w-48 overflow-hidden rounded-2xl border border-white/10 bg-slate-800/95 backdrop-blur-xl"
                >
                  {dataMenuItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className="block px-4 py-3 text-slate-300 transition-colors hover:bg-white/5 hover:text-white"
                    >
                      {item.label}
                    </Link>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Advanced Dropdown */}
          <div
            className="relative"
            onMouseEnter={() => setIsAdvancedOpen(true)}
            onMouseLeave={() => setIsAdvancedOpen(false)}
          >
            <button className="flex items-center gap-1 text-slate-300 transition-colors hover:text-white">
              고급 분석
              <ChevronDown className={`h-4 w-4 transition-transform ${isAdvancedOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
              {isAdvancedOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.2 }}
                  className="absolute left-0 top-full mt-2 w-56 overflow-hidden rounded-2xl border border-white/10 bg-slate-800/95 backdrop-blur-xl"
                >
                  {advancedMenuItems.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className="flex items-center justify-between px-4 py-3 text-slate-300 transition-colors hover:bg-white/5 hover:text-white"
                    >
                      {item.label}
                      {item.badge && (
                        <span className="rounded-full bg-gradient-to-r from-orange-500 to-red-500 px-2 py-0.5 text-xs font-bold text-white">
                          {item.badge}
                        </span>
                      )}
                    </Link>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Right Side */}
        <div className="hidden items-center gap-4 lg:flex">
          <UsageIndicator />

          <Link href="/login">
            <button className="rounded-xl px-4 py-2 text-slate-300 transition-colors hover:text-white">
              로그인
            </button>
          </Link>

          <Link href="/register">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <div className="group relative overflow-hidden rounded-xl">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
                <div className="relative flex items-center gap-2 px-6 py-2 text-sm font-semibold text-white">
                  <Sparkles className="h-4 w-4" />
                  무료 시작
                </div>
              </div>
            </motion.div>
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="lg:hidden text-white"
        >
          {isMobileMenuOpen ? <X /> : <Menu />}
        </button>
      </nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-white/10 bg-slate-900/95 backdrop-blur-xl lg:hidden"
          >
            <div className="container mx-auto px-4 py-4">
              <div className="space-y-2">
                {[...analysisMenuItems, ...dataMenuItems, ...advancedMenuItems].map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className="block rounded-lg px-4 py-3 text-slate-300 transition-colors hover:bg-white/5 hover:text-white"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {item.label}
                  </Link>
                ))}
                <div className="pt-4 border-t border-white/10 space-y-2">
                  <Link href="/login" className="block rounded-lg px-4 py-3 text-center text-slate-300">
                    로그인
                  </Link>
                  <Link href="/register" className="block rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-3 text-center font-semibold text-white">
                    무료 시작
                  </Link>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
