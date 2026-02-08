"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useRentVsJeonse } from "@/hooks/useRentVsJeonse";
import RegionFilter from "@/components/filters/RegionFilter";
import RentJeonsePieChart from "@/components/charts/RentJeonsePieChart";
import RentJeonseBarChart from "@/components/charts/RentJeonseBarChart";
import RentJeonseTrendChart from "@/components/charts/RentJeonseTrendChart";
import RentJeonseAreaChart from "@/components/charts/RentJeonseAreaChart";
import { HomeIcon, TrendingUp, AlertCircle, Info, BarChart3 } from "lucide-react";

export default function RentVsJeonsePage() {
  const [region, setRegion] = useState<string>("all");

  const { data, isLoading, error } = useRentVsJeonse({ regionFilter: region });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
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
              월세/전세 분석
            </motion.h1>
            <p className="text-lg text-slate-400">월세 전환율과 전월세 선호도를 분석합니다</p>
          </div>

          <div className="space-y-8">
            <div className="h-16 animate-pulse rounded-2xl bg-white/5"></div>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-32 animate-pulse rounded-2xl bg-white/5"></div>
              ))}
            </div>
            <div className="h-96 animate-pulse rounded-3xl bg-white/5"></div>
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
              월세/전세 분석
            </h1>
            <p className="text-lg text-slate-400">월세 전환율과 전월세 선호도를 분석합니다</p>
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

  if (!data?.success || !data?.data || !data.data.has_data) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              월세/전세 분석
            </h1>
            <p className="text-lg text-slate-400">월세 전환율과 전월세 선호도를 분석합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <HomeIcon className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">{data?.data?.message || "표시할 전월세 데이터가 없습니다"}</p>
          </div>
        </div>
      </div>
    );
  }

  const { stats, by_region, by_area, by_floor, by_deposit, trend } = data.data;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-600/20 via-pink-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
          animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute right-1/3 top-40 h-80 w-80 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 opacity-10 blur-3xl"
          animate={{ y: [0, -30, 0], scale: [1, 1.1, 1] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
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
            <HomeIcon className="h-4 w-4 text-purple-400" />
            <span className="text-sm font-semibold text-purple-300">전월세 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-purple-100 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
            월세/전세 분석
          </h1>
          <p className="text-xl text-slate-400">월세 전환율과 전월세 선호도를 분석합니다</p>
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

        {/* Info Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="mb-12 overflow-hidden rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/5 p-6 backdrop-blur-sm"
        >
          <div className="flex items-start gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/20">
              <Info className="h-5 w-5 text-blue-400" />
            </div>
            <div>
              <h3 className="mb-2 text-sm font-semibold text-blue-300">월세 전환율이란?</h3>
              <p className="text-sm text-blue-400/80">
                월세 전환율 = (월세 × 12) ÷ 보증금 × 100 (연 환산)
                <br />
                은행 금리보다 높으면 월세가 유리, 낮으면 전세가 유리합니다. 일반적으로 4~6%가 적정 수준입니다.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Comparison Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-16"
        >
          <h2 className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent">
            전월세 비교
          </h2>

          {/* Stats Cards */}
          <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { title: "전세 거래", value: `${stats.jeonse_count.toLocaleString("ko-KR")}건`, subtitle: `${stats.jeonse_ratio.toFixed(1)}%`, gradient: "from-blue-400 to-cyan-400" },
              { title: "월세 거래", value: `${stats.wolse_count.toLocaleString("ko-KR")}건`, subtitle: `${stats.wolse_ratio.toFixed(1)}%`, gradient: "from-red-400 to-rose-400" },
              { title: "평균 월세 전환율", value: `${stats.avg_conversion_rate.toFixed(2)}%`, subtitle: "Average Rate", gradient: "from-purple-400 to-pink-400" },
              { title: "중앙 월세 전환율", value: `${stats.median_conversion_rate.toFixed(2)}%`, subtitle: "Median Rate", gradient: "from-indigo-400 to-violet-400" },
            ].map((stat, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:from-white/10"
              >
                <div className={`absolute -inset-1 bg-gradient-to-r ${stat.gradient} opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20`}></div>
                <div className="relative">
                  <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r ${stat.gradient}`}>
                    <BarChart3 className="h-6 w-6 text-white" />
                  </div>
                  <p className="mb-2 text-sm text-slate-400">{stat.title}</p>
                  <p className={`mb-1 bg-gradient-to-r ${stat.gradient} bg-clip-text text-3xl font-bold text-transparent`}>
                    {stat.value}
                  </p>
                  <p className="text-xs text-slate-500">{stat.subtitle}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Charts */}
          <div className="mb-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <RentJeonsePieChart stats={stats} />
            </div>
            {by_region.length > 0 && (
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <RentJeonseBarChart data={by_region} />
              </div>
            )}
          </div>

          {/* Regional Table */}
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
            <div className="border-b border-white/10 p-6">
              <h3 className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
                지역별 전월세 상세 통계
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="border-b border-white/10">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                      지역
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      전세 건수
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      월세 건수
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      전세 비율
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      월세 비율
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      평균 전환율
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {by_region.map((item, idx) => (
                    <tr key={idx} className="transition-colors hover:bg-white/5">
                      <td className="px-4 py-3 text-sm text-white">{item.region}</td>
                      <td className="px-4 py-3 text-right text-sm text-blue-300">
                        {item.jeonse_count.toLocaleString("ko-KR")}
                      </td>
                      <td className="px-4 py-3 text-right text-sm text-red-300">
                        {item.wolse_count.toLocaleString("ko-KR")}
                      </td>
                      <td className="px-4 py-3 text-right text-sm text-white">
                        {item.jeonse_ratio.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-right text-sm text-white">
                        {item.wolse_ratio.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-right text-sm text-white">
                        {item.avg_conversion_rate.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.section>

        {/* Trend Section */}
        {trend && trend.length > 0 && (
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-16"
          >
            <h2 className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent">
              전월세 추이
            </h2>

            <div className="mb-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <RentJeonseTrendChart data={trend} />
              </div>
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <RentJeonseAreaChart data={trend} />
              </div>
            </div>

            {/* Monthly Table */}
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="border-b border-white/10 p-6">
                <h3 className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
                  월별 전월세 통계
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-white/10">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                        월
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        전세 건수
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        월세 건수
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        전세 비율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균 전환율
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {trend.map((item, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-white/5">
                        <td className="px-4 py-3 text-sm text-white">{item.year_month}</td>
                        <td className="px-4 py-3 text-right text-sm text-blue-300">
                          {item.jeonse_count.toLocaleString("ko-KR")}
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-red-300">
                          {item.wolse_count.toLocaleString("ko-KR")}
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {item.jeonse_ratio.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {item.avg_conversion_rate.toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </motion.section>
        )}

        {/* Additional Analysis Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h2 className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent">
            추가 분석
          </h2>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* By Area Table */}
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="border-b border-white/10 p-6">
                <h3 className="text-lg font-semibold text-white">면적대별 전월세 비율</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-white/10">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                        면적대
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        전세 비율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        월세 비율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        전환율
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {by_area.map((item, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-white/5">
                        <td className="px-4 py-3 text-sm text-white">{item.area_range}</td>
                        <td className="px-4 py-3 text-right text-sm text-blue-300">
                          {item.jeonse_ratio.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-red-300">
                          {item.wolse_ratio.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {item.avg_conversion_rate.toFixed(2)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* By Floor Table */}
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="border-b border-white/10 p-6">
                <h3 className="text-lg font-semibold text-white">층수별 전월세 선호도</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-white/10">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                        층수 구간
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        전세 비율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        월세 비율
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {by_floor.map((item, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-white/5">
                        <td className="px-4 py-3 text-sm text-white">{item.floor_category}</td>
                        <td className="px-4 py-3 text-right text-sm text-blue-300">
                          {item.jeonse_ratio.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-red-300">
                          {item.wolse_ratio.toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* By Deposit Table */}
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm lg:col-span-2">
              <div className="border-b border-white/10 p-6">
                <h3 className="text-lg font-semibold text-white">보증금 구간별 월세 전환율</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-white/10">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                        보증금 구간
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        건수
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균 전환율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균 월세
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균 보증금
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {by_deposit.map((item, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-white/5">
                        <td className="px-4 py-3 text-sm text-white">{item.deposit_range}</td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {item.count.toLocaleString("ko-KR")}
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {item.avg_conversion_rate.toFixed(2)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {item.avg_monthly_rent.toLocaleString("ko-KR")}만원
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {Math.round(item.avg_deposit / 10000).toLocaleString("ko-KR")}억원
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
}
