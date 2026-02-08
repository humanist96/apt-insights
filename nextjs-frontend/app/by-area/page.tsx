"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useByArea } from "@/hooks/useByArea";
import RegionFilter from "@/components/filters/RegionFilter";
import AreaBinsSelector from "@/components/AreaBinsSelector";
import AreaDistributionChart from "@/components/charts/AreaDistributionChart";
import AreaPriceChart from "@/components/charts/AreaPriceChart";
import AreaPricePerAreaChart from "@/components/charts/AreaPricePerAreaChart";
import { Maximize2, BarChart3, TrendingUp, AlertCircle, DollarSign } from "lucide-react";

const DEFAULT_BINS = [50, 60, 85, 100, 135];

export default function ByAreaPage() {
  const [region, setRegion] = useState<string>("all");
  const [bins, setBins] = useState<number[]>(DEFAULT_BINS);

  const { data, isLoading, error } = useByArea({ region, bins });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
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
              면적별 분석
            </motion.h1>
            <p className="text-lg text-slate-400">전용면적에 따른 거래 현황을 분석합니다</p>
          </div>

          <div className="space-y-8">
            <div className="h-16 w-64 animate-pulse rounded-2xl bg-white/5"></div>
            <div className="h-32 animate-pulse rounded-2xl bg-white/5"></div>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              {[1, 2].map((i) => (
                <div key={i} className="h-32 animate-pulse rounded-2xl bg-white/5"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-96 animate-pulse rounded-2xl bg-white/5"></div>
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
              면적별 분석
            </h1>
            <p className="text-lg text-slate-400">전용면적에 따른 거래 현황을 분석합니다</p>
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
              면적별 분석
            </h1>
            <p className="text-lg text-slate-400">전용면적에 따른 거래 현황을 분석합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <Maximize2 className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const areaData = data.data.data;
  const summary = data.data.summary;

  const totalTransactions = summary.total_transactions;
  const mostCommonRange = summary.most_common_range;

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
            ease: "easeInOut",
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
            ease: "easeInOut",
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
            <Maximize2 className="h-4 w-4 text-blue-400" />
            <span className="text-sm font-semibold text-blue-300">면적 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-5xl font-bold text-transparent">
            면적별 분석
          </h1>
          <p className="text-xl text-slate-400">전용면적에 따른 거래 현황을 분석합니다</p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 space-y-4"
        >
          <RegionFilter value={region} onChange={setRegion} />

          <div className="overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
            <AreaBinsSelector bins={bins} onChange={setBins} />
          </div>
        </motion.div>

        {/* Stats Cards */}
        {areaData.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-12 grid grid-cols-1 gap-6 sm:grid-cols-2"
          >
            <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:border-blue-500/30 hover:from-white/10">
              <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-cyan-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>
              <div className="relative">
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500">
                  <BarChart3 className="h-6 w-6 text-white" />
                </div>
                <p className="mb-2 text-sm text-slate-400">총 거래 건수</p>
                <p className="mb-1 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-3xl font-bold text-transparent">
                  {totalTransactions.toLocaleString("ko-KR")}
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
                <p className="mb-2 text-sm text-slate-400">가장 많은 거래 면적대</p>
                <p className="mb-1 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-3xl font-bold text-transparent">
                  {mostCommonRange ? mostCommonRange.area_range.replace("~", "-") + "㎡" : "N/A"}
                </p>
                <p className="text-xs text-slate-500">
                  {mostCommonRange ? `${mostCommonRange.count.toLocaleString("ko-KR")}건` : ""}
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Charts and Table */}
        {areaData.length > 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <AreaDistributionChart data={areaData} />
              </div>
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <AreaPriceChart data={areaData} />
              </div>
            </div>

            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <AreaPricePerAreaChart data={areaData} />
            </div>

            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="border-b border-white/10 p-6">
                <h3 className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
                  면적대별 상세 통계
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-white/10">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                        면적구간 (㎡)
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        거래건수
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균가격
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        중앙가격
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        최고가격
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        최저가격
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        평균면적
                      </th>
                      <th className="px-6 py-4 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                        ㎡당 가격
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {areaData.map((item, index) => (
                      <motion.tr
                        key={index}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: index * 0.05 }}
                        className="transition-colors hover:bg-white/5"
                      >
                        <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-white">
                          {item.area_range.replace("~", " - ")}
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {item.count.toLocaleString("ko-KR")}
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {Math.round(item.avg_price / 10000).toLocaleString("ko-KR")}억
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {Math.round(item.median_price / 10000).toLocaleString("ko-KR")}억
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {item.max_price ? `${Math.round(item.max_price / 10000).toLocaleString("ko-KR")}억` : "N/A"}
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {item.min_price ? `${Math.round(item.min_price / 10000).toLocaleString("ko-KR")}억` : "N/A"}
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {item.avg_area.toFixed(1)}㎡
                        </td>
                        <td className="whitespace-nowrap px-6 py-4 text-right text-sm text-white">
                          {Math.round(item.price_per_area).toLocaleString("ko-KR")}만
                        </td>
                      </motion.tr>
                    ))}
                  </tbody>
                </table>
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
              <Maximize2 className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">선택한 조건에 맞는 데이터가 없습니다</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
