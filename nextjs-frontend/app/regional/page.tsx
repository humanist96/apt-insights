"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useRegionalAnalysis } from "@/hooks/useRegionalAnalysis";
import RegionFilter from "@/components/filters/RegionFilter";
import RegionalBarChart from "@/components/charts/RegionalBarChart";
import RegionalPieChart from "@/components/charts/RegionalPieChart";
import StatsCard from "@/components/stats/StatsCard";
import { BarChart3, TrendingUp, MapPin, AlertCircle } from "lucide-react";

export default function RegionalPage() {
  const [region, setRegion] = useState<string>("all");
  const { data, isLoading, error } = useRegionalAnalysis(region);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        {/* Animated Background */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 opacity-10 blur-3xl"
            animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>

        <div className="container relative mx-auto px-4 py-16">
          <div className="mb-12">
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent"
            >
              지역별 분석
            </motion.h1>
            <p className="text-lg text-slate-400">지역별 아파트 거래 현황을 분석합니다</p>
          </div>

          {/* Loading Skeleton */}
          <div className="space-y-8">
            <div className="h-16 w-64 animate-pulse rounded-2xl bg-white/5"></div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="h-32 animate-pulse rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"
                ></motion.div>
              ))}
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="h-96 animate-pulse rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"></div>
              <div className="h-96 animate-pulse rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              지역별 분석
            </h1>
            <p className="text-lg text-slate-400">지역별 아파트 거래 현황을 분석합니다</p>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="overflow-hidden rounded-3xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 p-8 backdrop-blur-sm"
          >
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-red-500/20">
                <AlertCircle className="h-6 w-6 text-red-400" />
              </div>
              <div>
                <h3 className="mb-2 text-xl font-semibold text-red-300">
                  데이터를 불러오는 중 오류가 발생했습니다
                </h3>
                <p className="text-red-400/80">
                  {error instanceof Error ? error.message : "알 수 없는 오류가 발생했습니다"}
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  if (!data?.success || !data?.data) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              지역별 분석
            </h1>
            <p className="text-lg text-slate-400">지역별 아파트 거래 현황을 분석합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <BarChart3 className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const { by_region, summary } = data.data;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-600/20 via-purple-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 opacity-10 blur-3xl"
          animate={{
            y: [0, 50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute right-1/3 top-40 h-80 w-80 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
          animate={{
            y: [0, -30, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      </div>

      <div className="container relative mx-auto px-4 py-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2">
            <MapPin className="h-4 w-4 text-blue-400" />
            <span className="text-sm font-semibold text-blue-300">지역 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-5xl font-bold text-transparent">
            지역별 분석
          </h1>
          <p className="text-xl text-slate-400">지역별 아파트 거래 현황을 분석합니다</p>
        </motion.div>

        {/* Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <RegionFilter value={region} onChange={setRegion} />
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:border-blue-500/30 hover:from-white/10">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-cyan-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">총 거래 건수</p>
              <p className="mb-1 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-3xl font-bold text-transparent">
                {summary.total_transactions.toLocaleString("ko-KR")}
              </p>
              <p className="text-xs text-slate-500">Total Transactions</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:border-purple-500/30 hover:from-white/10">
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-pink-500">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">평균 거래 가격</p>
              <p className="mb-1 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-3xl font-bold text-transparent">
                {Math.round(summary.average_price / 10000).toLocaleString("ko-KR")}억원
              </p>
              <p className="text-xs text-slate-500">Average Price</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:border-green-500/30 hover:from-white/10">
            <div className="absolute -inset-1 bg-gradient-to-r from-green-500 to-emerald-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-green-500 to-emerald-500">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">최고가 지역</p>
              <p className="mb-1 bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-3xl font-bold text-transparent">
                {summary.highest_region
                  ? `${Math.round(summary.highest_region.avg_price / 10000).toLocaleString("ko-KR")}억원`
                  : "-"}
              </p>
              <p className="text-xs text-slate-500">{summary.highest_region?.region || "N/A"}</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:border-amber-500/30 hover:from-white/10">
            <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 to-orange-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-amber-500 to-orange-500">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">최저가 지역</p>
              <p className="mb-1 bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-3xl font-bold text-transparent">
                {summary.lowest_region
                  ? `${Math.round(summary.lowest_region.avg_price / 10000).toLocaleString("ko-KR")}억원`
                  : "-"}
              </p>
              <p className="text-xs text-slate-500">{summary.lowest_region?.region || "N/A"}</p>
            </div>
          </div>
        </motion.div>

        {/* Charts */}
        {by_region.length > 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="grid grid-cols-1 gap-6 lg:grid-cols-2"
          >
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <RegionalBarChart data={by_region} />
            </div>
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <RegionalPieChart data={by_region} />
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm"
          >
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <BarChart3 className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">선택한 지역에 대한 데이터가 없습니다</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
