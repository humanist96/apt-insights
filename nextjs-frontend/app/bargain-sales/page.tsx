"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useBargainSales } from "@/hooks/useBargainSales";
import RegionFilter from "@/components/filters/RegionFilter";
import StatsCard from "@/components/stats/StatsCard";
import BargainSalesScatter from "@/components/charts/BargainSalesScatter";
import BargainDistributionChart from "@/components/charts/BargainDistributionChart";
import BargainSalesTable from "@/components/BargainSalesTable";
import { Zap, TrendingDown, Percent, DollarSign, AlertCircle, Info } from "lucide-react";

export default function BargainSalesPage() {
  const [region, setRegion] = useState<string>("all");
  const [thresholdPct, setThresholdPct] = useState<number>(15);
  const [minTransactionCount, setMinTransactionCount] = useState<number>(2);

  const {
    data: bargainData,
    isLoading,
    error,
  } = useBargainSales({
    regionFilter: region,
    thresholdPct,
    minTransactionCount,
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute right-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-red-500 to-orange-600 opacity-10 blur-3xl"
            animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>

        <div className="container relative mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              급매물 탐지 분석
            </h1>
            <p className="text-lg text-slate-400">
              동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
            </p>
          </div>

          <div className="space-y-8 animate-pulse">
            <div className="h-12 w-64 rounded-xl bg-white/5 border border-white/10"></div>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-32 rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0"></div>
              ))}
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
              급매물 탐지 분석
            </h1>
            <p className="text-lg text-slate-400">
              동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
            </p>
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

  if (!bargainData?.success || !bargainData?.data) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              급매물 탐지 분석
            </h1>
            <p className="text-lg text-slate-400">
              동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
            </p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <Zap className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const { bargain_items, stats, by_region } = bargainData.data;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-red-600/20 via-orange-600/10 to-transparent"></div>
        <motion.div
          className="absolute right-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-red-500 to-orange-600 opacity-10 blur-3xl"
          animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      <div className="container relative mx-auto px-4 py-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-4 py-2">
            <Zap className="h-4 w-4 text-red-400" />
            <span className="text-sm font-semibold text-red-300">급매물 탐지</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-red-100 to-orange-200 bg-clip-text text-5xl font-bold text-transparent">
            급매물 탐지 분석
          </h1>
          <p className="text-xl text-slate-400">
            동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
          </p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 space-y-6"
        >
          <RegionFilter value={region} onChange={setRegion} />

          <div className="overflow-hidden rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-blue-600/5 p-6 backdrop-blur-sm">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-500/20">
                <Info className="h-5 w-5 text-blue-400" />
              </div>
              <div>
                <h3 className="mb-1 font-semibold text-blue-300">급매물 탐지 기준</h3>
                <p className="text-sm text-blue-400/80">
                  동일 아파트의 같은 면적대(±5㎡)에서 최근 5건 평균가 대비 {thresholdPct}% 이상
                  낮은 거래를 급매물로 판정합니다.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-6">
            <div className="flex-1 min-w-[250px]">
              <label className="mb-3 block text-sm font-medium text-slate-300">
                할인율 기준: <span className="text-orange-400 font-bold">{thresholdPct}%</span>
              </label>
              <input
                type="range"
                min="10"
                max="30"
                step="5"
                value={thresholdPct}
                onChange={(e) => setThresholdPct(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gradient-to-r [&::-webkit-slider-thumb]:from-red-500 [&::-webkit-slider-thumb]:to-orange-500"
              />
              <div className="mt-2 flex justify-between text-xs text-slate-500">
                <span>10%</span>
                <span>15%</span>
                <span>20%</span>
                <span>25%</span>
                <span>30%</span>
              </div>
            </div>

            <div className="flex-1 min-w-[250px]">
              <label className="mb-3 block text-sm font-medium text-slate-300">
                최소 거래 건수: <span className="text-orange-400 font-bold">{minTransactionCount}건</span>
              </label>
              <input
                type="range"
                min="2"
                max="10"
                step="1"
                value={minTransactionCount}
                onChange={(e) => setMinTransactionCount(Number(e.target.value))}
                className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gradient-to-r [&::-webkit-slider-thumb]:from-red-500 [&::-webkit-slider-thumb]:to-orange-500"
              />
              <div className="mt-2 flex justify-between text-xs text-slate-500">
                <span>2건</span>
                <span>5건</span>
                <span>10건</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-red-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-red-500 to-rose-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-red-500 to-rose-500">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">급매물 수</p>
              <p className="mb-1 bg-gradient-to-r from-red-400 to-rose-400 bg-clip-text text-3xl font-bold text-transparent">
                {stats.bargain_count.toLocaleString("ko-KR")}건
              </p>
              <p className="text-xs text-slate-500">Bargain Count</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-orange-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-orange-500 to-amber-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-orange-500 to-amber-500">
                <TrendingDown className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">평균 할인율</p>
              <p className="mb-1 bg-gradient-to-r from-orange-400 to-amber-400 bg-clip-text text-3xl font-bold text-transparent">
                {stats.avg_discount.toFixed(1)}%
              </p>
              <p className="text-xs text-slate-500">Average Discount</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-amber-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 to-yellow-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-amber-500 to-yellow-500">
                <Percent className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">최대 할인율</p>
              <p className="mb-1 bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-3xl font-bold text-transparent">
                {stats.max_discount.toFixed(1)}%
              </p>
              <p className="text-xs text-slate-500">Maximum Discount</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-blue-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-cyan-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500">
                <DollarSign className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">총 절감액</p>
              <p className="mb-1 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-3xl font-bold text-transparent">
                {Math.round(stats.total_savings / 10000).toLocaleString("ko-KR")}억원
              </p>
              <p className="text-xs text-slate-500">Total Savings</p>
            </div>
          </div>
        </motion.div>

        {/* Category Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-12 grid grid-cols-1 gap-4 sm:grid-cols-4"
        >
          <div className="overflow-hidden rounded-2xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 p-6 backdrop-blur-sm">
            <h3 className="mb-1 text-sm font-semibold text-red-300">초특급 급매</h3>
            <p className="mb-3 text-xs text-red-400/80">25% 이상 할인</p>
            <p className="bg-gradient-to-r from-red-400 to-rose-400 bg-clip-text text-3xl font-bold text-transparent">
              {bargain_items.filter((item) => item.discount_pct >= 25).length}건
            </p>
          </div>

          <div className="overflow-hidden rounded-2xl border border-orange-500/20 bg-gradient-to-br from-orange-500/10 to-orange-600/5 p-6 backdrop-blur-sm">
            <h3 className="mb-1 text-sm font-semibold text-orange-300">특급 급매</h3>
            <p className="mb-3 text-xs text-orange-400/80">20-25% 할인</p>
            <p className="bg-gradient-to-r from-orange-400 to-amber-400 bg-clip-text text-3xl font-bold text-transparent">
              {bargain_items.filter((item) => item.discount_pct >= 20 && item.discount_pct < 25).length}건
            </p>
          </div>

          <div className="overflow-hidden rounded-2xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-amber-600/5 p-6 backdrop-blur-sm">
            <h3 className="mb-1 text-sm font-semibold text-amber-300">일반 급매</h3>
            <p className="mb-3 text-xs text-amber-400/80">15-20% 할인</p>
            <p className="bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-3xl font-bold text-transparent">
              {bargain_items.filter((item) => item.discount_pct >= 15 && item.discount_pct < 20).length}건
            </p>
          </div>

          <div className="overflow-hidden rounded-2xl border border-emerald-500/20 bg-gradient-to-br from-emerald-500/10 to-emerald-600/5 p-6 backdrop-blur-sm">
            <h3 className="mb-1 text-sm font-semibold text-emerald-300">경미 할인</h3>
            <p className="mb-3 text-xs text-emerald-400/80">15% 미만 할인</p>
            <p className="bg-gradient-to-r from-emerald-400 to-green-400 bg-clip-text text-3xl font-bold text-transparent">
              {bargain_items.filter((item) => item.discount_pct < 15).length}건
            </p>
          </div>
        </motion.div>

        {/* Charts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="space-y-6"
        >
          {by_region.length > 0 && (
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <BargainDistributionChart data={by_region} />
            </div>
          )}

          {bargain_items.length > 0 && (
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <BargainSalesScatter data={bargain_items} />
            </div>
          )}

          {bargain_items.length > 0 && (
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="p-6">
                <BargainSalesTable data={bargain_items} />
              </div>
            </div>
          )}

          {bargain_items.length === 0 && (
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
                <Zap className="h-8 w-8 text-slate-400" />
              </div>
              <p className="mb-2 text-lg text-slate-400">선택한 조건에 해당하는 급매물이 없습니다.</p>
              <p className="text-sm text-slate-500">할인율 기준을 낮추거나 다른 지역을 선택해 보세요.</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
