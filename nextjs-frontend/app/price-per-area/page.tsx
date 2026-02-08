"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { usePricePerArea } from "@/hooks/usePricePerArea";
import { usePricePerAreaTrend } from "@/hooks/usePricePerAreaTrend";
import RegionFilter from "@/components/filters/RegionFilter";
import PricePerAreaBarChart from "@/components/charts/PricePerAreaBarChart";
import PricePerAreaBoxPlot from "@/components/charts/PricePerAreaBoxPlot";
import PricePerAreaTrendChart from "@/components/charts/PricePerAreaTrendChart";
import { DollarSign, TrendingUp, TrendingDown, BarChart3, AlertCircle, Calendar } from "lucide-react";

export default function PricePerAreaPage() {
  const [region, setRegion] = useState<string>("all");
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");

  const { data, isLoading, error } = usePricePerArea({
    regionFilter: region !== "all" ? region : undefined,
    startDate,
    endDate,
  });

  const {
    data: trendData,
    isLoading: trendLoading,
    error: trendError,
  } = usePricePerAreaTrend({
    regionFilter: region !== "all" ? region : undefined,
    startDate,
    endDate,
  });

  if (isLoading || trendLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 opacity-10 blur-3xl"
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
              평당가 분석
            </motion.h1>
            <p className="text-lg text-slate-400">면적당 가격을 분석하여 투자 가치를 평가합니다</p>
          </div>

          <div className="space-y-8">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-12 animate-pulse rounded-xl bg-white/5"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-32 animate-pulse rounded-2xl bg-white/5"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="h-96 animate-pulse rounded-3xl bg-white/5"></div>
              <div className="h-96 animate-pulse rounded-3xl bg-white/5"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || trendError) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              평당가 분석
            </h1>
            <p className="text-lg text-slate-400">면적당 가격을 분석하여 투자 가치를 평가합니다</p>
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
                  {error instanceof Error
                    ? error.message
                    : trendError instanceof Error
                      ? trendError.message
                      : "알 수 없는 오류가 발생했습니다"}
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  if (!data?.success || !data?.data || !trendData?.success || !trendData?.data) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              평당가 분석
            </h1>
            <p className="text-lg text-slate-400">면적당 가격을 분석하여 투자 가치를 평가합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <DollarSign className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const { stats, by_region, by_area_range, top_expensive, top_affordable } = data.data;
  const { trend } = trendData.data;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-green-600/20 via-emerald-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 opacity-10 blur-3xl"
          animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute right-1/3 top-40 h-80 w-80 rounded-full bg-gradient-to-r from-blue-500 to-cyan-600 opacity-10 blur-3xl"
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
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/10 px-4 py-2">
            <DollarSign className="h-4 w-4 text-green-400" />
            <span className="text-sm font-semibold text-green-300">평당가 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-green-100 to-emerald-200 bg-clip-text text-5xl font-bold text-transparent">
            평당가 분석
          </h1>
          <p className="text-xl text-slate-400">면적당 가격을 분석하여 투자 가치를 평가합니다</p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3"
        >
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">지역 선택</label>
            <RegionFilter value={region} onChange={setRegion} />
          </div>

          <div>
            <label htmlFor="start-date" className="mb-2 block text-sm font-medium text-slate-300">
              시작일
            </label>
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                <Calendar className="h-5 w-5 text-slate-400" />
              </div>
              <input
                type="month"
                id="start-date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-white/5 py-3 pl-12 pr-4 text-white placeholder-slate-500 backdrop-blur-sm transition-all focus:border-green-500/50 focus:outline-none focus:ring-2 focus:ring-green-500/20"
              />
            </div>
          </div>

          <div>
            <label htmlFor="end-date" className="mb-2 block text-sm font-medium text-slate-300">
              종료일
            </label>
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                <Calendar className="h-5 w-5 text-slate-400" />
              </div>
              <input
                type="month"
                id="end-date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full rounded-xl border border-white/10 bg-white/5 py-3 pl-12 pr-4 text-white placeholder-slate-500 backdrop-blur-sm transition-all focus:border-green-500/50 focus:outline-none focus:ring-2 focus:ring-green-500/20"
              />
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
          {[
            { title: "평균 평당가", value: stats.avg_price_per_area, gradient: "from-green-500 to-emerald-500", icon: BarChart3 },
            { title: "중앙 평당가", value: stats.median_price_per_area, gradient: "from-blue-500 to-cyan-500", icon: TrendingUp },
            { title: "최고 평당가", value: stats.max_price_per_area, gradient: "from-red-500 to-rose-500", icon: TrendingUp },
            { title: "최저 평당가", value: stats.min_price_per_area, gradient: "from-amber-500 to-orange-500", icon: TrendingDown },
          ].map((stat, index) => (
            <div
              key={index}
              className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:border-green-500/30 hover:from-white/10"
            >
              <div className={`absolute -inset-1 bg-gradient-to-r ${stat.gradient} opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20`}></div>
              <div className="relative">
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r ${stat.gradient}`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <p className="mb-2 text-sm text-slate-400">{stat.title}</p>
                <p className={`mb-1 bg-gradient-to-r ${stat.gradient.replace("to-", "to-")} bg-clip-text text-3xl font-bold text-transparent`}>
                  {Math.round(stat.value).toLocaleString("ko-KR")}
                </p>
                <p className="text-xs text-slate-500">만원/㎡</p>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Charts */}
        {by_area_range.length > 0 && by_region.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-12 grid grid-cols-1 gap-6 lg:grid-cols-2"
          >
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <PricePerAreaBarChart data={by_area_range} />
            </div>
            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <PricePerAreaBoxPlot data={by_region} />
            </div>
          </motion.div>
        )}

        {/* Top Expensive/Affordable Tables */}
        {(top_expensive.length > 0 || top_affordable.length > 0) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mb-12 overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"
          >
            <div className="border-b border-white/10 p-6">
              <h3 className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
                평당가 상위 아파트
              </h3>
            </div>
            <div className="grid grid-cols-1 gap-6 p-6 lg:grid-cols-2">
              {top_expensive.length > 0 && (
                <div>
                  <h4 className="mb-4 flex items-center gap-2 text-lg font-semibold text-red-300">
                    <TrendingUp className="h-5 w-5" />
                    최고가 TOP 10
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead className="border-b border-white/10">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase text-slate-400">
                            아파트
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase text-slate-400">
                            평당가
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase text-slate-400">
                            면적
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-white/5">
                        {top_expensive.map((item, index) => (
                          <tr key={index} className="transition-colors hover:bg-white/5">
                            <td className="px-4 py-3 text-sm text-white">
                              <div>{item.apt_name}</div>
                              <div className="text-xs text-slate-500">{item.region}</div>
                            </td>
                            <td className="px-4 py-3 text-right text-sm text-white">
                              {Math.round(item.price_per_area).toLocaleString("ko-KR")}만
                            </td>
                            <td className="px-4 py-3 text-right text-sm text-white">
                              {item.area.toFixed(1)}㎡
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {top_affordable.length > 0 && (
                <div>
                  <h4 className="mb-4 flex items-center gap-2 text-lg font-semibold text-green-300">
                    <TrendingDown className="h-5 w-5" />
                    최저가 TOP 10
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead className="border-b border-white/10">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase text-slate-400">
                            아파트
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase text-slate-400">
                            평당가
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase text-slate-400">
                            면적
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-white/5">
                        {top_affordable.map((item, index) => (
                          <tr key={index} className="transition-colors hover:bg-white/5">
                            <td className="px-4 py-3 text-sm text-white">
                              <div>{item.apt_name}</div>
                              <div className="text-xs text-slate-500">{item.region}</div>
                            </td>
                            <td className="px-4 py-3 text-right text-sm text-white">
                              {Math.round(item.price_per_area).toLocaleString("ko-KR")}만
                            </td>
                            <td className="px-4 py-3 text-right text-sm text-white">
                              {item.area.toFixed(1)}㎡
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* Trend Section */}
        {trend.length > 0 && (
          <>
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent"
            >
              평당가 추이
            </motion.h2>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="mb-12 overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm"
            >
              <PricePerAreaTrendChart data={trend} />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"
            >
              <div className="border-b border-white/10 p-6">
                <h3 className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
                  월별 평당가 통계
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-white/10">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                        년월
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균 평당가
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        중앙 평당가
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        거래 건수
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        변동률
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {trend.map((item) => (
                      <tr key={item.year_month} className="transition-colors hover:bg-white/5">
                        <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-white">
                          {item.year_month}
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {Math.round(item.avg_price_per_area).toLocaleString("ko-KR")}만원/㎡
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {Math.round(item.median_price_per_area).toLocaleString("ko-KR")}만원/㎡
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {item.count.toLocaleString("ko-KR")}건
                        </td>
                        <td
                          className={`whitespace-nowrap px-6 py-4 text-right text-sm font-medium ${
                            item.change_rate && item.change_rate > 0
                              ? "text-red-400"
                              : item.change_rate && item.change_rate < 0
                                ? "text-blue-400"
                                : "text-slate-400"
                          }`}
                        >
                          {item.change_rate
                            ? `${item.change_rate > 0 ? "+" : ""}${item.change_rate.toFixed(2)}%`
                            : "-"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </motion.div>
          </>
        )}
      </div>
    </div>
  );
}
