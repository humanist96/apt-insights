"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { usePriceTrend } from "@/hooks/usePriceTrend";
import PriceTrendLineChart from "@/components/charts/PriceTrendLineChart";
import TransactionVolumeChart from "@/components/charts/TransactionVolumeChart";
import CombinedPriceVolumeChart from "@/components/charts/CombinedPriceVolumeChart";
import StatsCard from "@/components/stats/StatsCard";
import RegionFilter from "@/components/filters/RegionFilter";
import { TrendingUp, Calendar, BarChart3, AlertCircle, ArrowUp, ArrowDown } from "lucide-react";

export default function PriceTrendPage() {
  const [region, setRegion] = useState<string>("all");
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [groupBy, setGroupBy] = useState<"month" | "quarter">("month");

  const { data, isLoading, error } = usePriceTrend({
    startDate,
    endDate,
    regionFilter: region !== "all" ? region : undefined,
    groupBy,
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute right-1/4 top-40 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
            animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>

        <div className="container relative mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              가격 추이 분석
            </h1>
            <p className="text-lg text-slate-400">시간에 따른 아파트 가격 변동을 분석합니다</p>
          </div>

          <div className="space-y-8 animate-pulse">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-12 rounded-xl bg-white/5 border border-white/10"></div>
              ))}
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-32 rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0"></div>
              ))}
            </div>

            <div className="h-96 rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0"></div>
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
              가격 추이 분석
            </h1>
            <p className="text-lg text-slate-400">시간에 따른 아파트 가격 변동을 분석합니다</p>
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
              가격 추이 분석
            </h1>
            <p className="text-lg text-slate-400">시간에 따른 아파트 가격 변동을 분석합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <TrendingUp className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const { trend_data, summary } = data.data;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-600/20 via-blue-600/10 to-transparent"></div>
        <motion.div
          className="absolute right-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
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
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-purple-500/20 bg-purple-500/10 px-4 py-2">
            <TrendingUp className="h-4 w-4 text-purple-400" />
            <span className="text-sm font-semibold text-purple-300">가격 추이</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-purple-100 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
            가격 추이 분석
          </h1>
          <p className="text-xl text-slate-400">시간에 따른 아파트 가격 변동을 분석합니다</p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-4"
        >
          <div>
            <label htmlFor="region-filter" className="mb-2 block text-sm font-medium text-slate-300">
              지역 선택
            </label>
            <RegionFilter value={region} onChange={setRegion} />
          </div>

          <div>
            <label htmlFor="start-date" className="mb-2 block text-sm font-medium text-slate-300">
              시작일
            </label>
            <input
              type="month"
              id="start-date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white backdrop-blur-sm transition-all focus:border-purple-500/50 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            />
          </div>

          <div>
            <label htmlFor="end-date" className="mb-2 block text-sm font-medium text-slate-300">
              종료일
            </label>
            <input
              type="month"
              id="end-date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white backdrop-blur-sm transition-all focus:border-purple-500/50 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            />
          </div>

          <div>
            <label htmlFor="group-by" className="mb-2 block text-sm font-medium text-slate-300">
              집계 단위
            </label>
            <select
              id="group-by"
              value={groupBy}
              onChange={(e) => setGroupBy(e.target.value as "month" | "quarter")}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white backdrop-blur-sm transition-all focus:border-purple-500/50 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
            >
              <option value="month" className="bg-slate-800">월별</option>
              <option value="quarter" className="bg-slate-800">분기별</option>
            </select>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-blue-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-cyan-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">총 기간</p>
              <p className="mb-1 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-3xl font-bold text-transparent">
                {summary.total_months}개월
              </p>
              <p className="text-xs text-slate-500">Total Months</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-purple-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-pink-500">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">전체 평균 가격</p>
              <p className="mb-1 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-3xl font-bold text-transparent">
                {Math.round(summary.overall_avg_price / 10000).toLocaleString("ko-KR")}억원
              </p>
              <p className="text-xs text-slate-500">Overall Average Price</p>
            </div>
          </div>

          <div className={`group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all ${summary.price_change_pct > 0 ? 'hover:border-green-500/30' : 'hover:border-red-500/30'}`}>
            <div className={`absolute -inset-1 bg-gradient-to-r ${summary.price_change_pct > 0 ? 'from-green-500 to-emerald-500' : 'from-red-500 to-rose-500'} opacity-0 blur-xl transition-opacity group-hover:opacity-20`}></div>
            <div className="relative">
              <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r ${summary.price_change_pct > 0 ? 'from-green-500 to-emerald-500' : 'from-red-500 to-rose-500'}`}>
                {summary.price_change_pct > 0 ? (
                  <ArrowUp className="h-6 w-6 text-white" />
                ) : (
                  <ArrowDown className="h-6 w-6 text-white" />
                )}
              </div>
              <p className="mb-2 text-sm text-slate-400">가격 변동률</p>
              <p className={`mb-1 bg-gradient-to-r ${summary.price_change_pct > 0 ? 'from-green-400 to-emerald-400' : 'from-red-400 to-rose-400'} bg-clip-text text-3xl font-bold text-transparent`}>
                {summary.price_change_pct > 0 ? "+" : ""}{summary.price_change_pct.toFixed(1)}%
              </p>
              <p className="text-xs text-slate-500">Price Change</p>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-amber-500/30">
            <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 to-orange-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
            <div className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-amber-500 to-orange-500">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <p className="mb-2 text-sm text-slate-400">총 거래 건수</p>
              <p className="mb-1 bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-3xl font-bold text-transparent">
                {summary.total_transactions.toLocaleString("ko-KR")}
              </p>
              <p className="text-xs text-slate-500">Total Transactions</p>
            </div>
          </div>
        </motion.div>

        {/* Charts */}
        {trend_data.length > 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <PriceTrendLineChart data={trend_data} />
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <TransactionVolumeChart data={trend_data} />
              </div>
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <CombinedPriceVolumeChart data={trend_data} />
              </div>
            </div>

            {/* Table */}
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="p-6">
                <h3 className="mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-2xl font-bold text-transparent">
                  월별 통계 테이블
                </h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full">
                    <thead>
                      <tr className="border-b border-white/10">
                        <th className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-slate-400">
                          년월
                        </th>
                        <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                          평균 가격
                        </th>
                        <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                          중앙 가격
                        </th>
                        <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                          거래 건수
                        </th>
                        <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                          최고가
                        </th>
                        <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">
                          최저가
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                      {trend_data.map((item, index) => (
                        <motion.tr
                          key={item.year_month}
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.05 * index }}
                          className="transition-colors hover:bg-white/5"
                        >
                          <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-white">
                            {item.year_month}
                          </td>
                          <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-slate-300">
                            {Math.round(item.avg_price / 10000).toLocaleString("ko-KR")}억원
                          </td>
                          <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-slate-300">
                            {Math.round(item.median_price / 10000).toLocaleString("ko-KR")}억원
                          </td>
                          <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-slate-300">
                            {item.count.toLocaleString("ko-KR")}건
                          </td>
                          <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-slate-300">
                            {Math.round(item.max_price / 10000).toLocaleString("ko-KR")}억원
                          </td>
                          <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-slate-300">
                            {Math.round(item.min_price / 10000).toLocaleString("ko-KR")}억원
                          </td>
                        </motion.tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
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
              <TrendingUp className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">선택한 기간에 대한 데이터가 없습니다</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
