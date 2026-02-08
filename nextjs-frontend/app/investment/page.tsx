"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useJeonseAnalysis } from "@/hooks/useJeonseAnalysis";
import { useGapInvestment } from "@/hooks/useGapInvestment";
import RegionFilter from "@/components/filters/RegionFilter";
import JeonseRatioChart from "@/components/charts/JeonseRatioChart";
import GapInvestmentScatter from "@/components/charts/GapInvestmentScatter";
import { PiggyBank, TrendingUp, AlertTriangle, Shield, Target, DollarSign, AlertCircle } from "lucide-react";

export default function InvestmentPage() {
  const [region, setRegion] = useState<string>("all");
  const [minJeonseRatio, setMinJeonseRatio] = useState<number>(0);
  const [minGapRatio, setMinGapRatio] = useState<number>(0);

  const {
    data: jeonseData,
    isLoading: jeonseLoading,
    error: jeonseError,
  } = useJeonseAnalysis({ regionFilter: region, minJeonseRatio });

  const {
    data: gapData,
    isLoading: gapLoading,
    error: gapError,
  } = useGapInvestment({ regionFilter: region, minGapRatio });

  const isLoading = jeonseLoading || gapLoading;
  const error = jeonseError || gapError;

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-amber-500 to-orange-600 opacity-10 blur-3xl"
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
              전세가율/갭투자 분석
            </motion.h1>
            <p className="text-lg text-slate-400">전세가율과 갭투자 기회를 분석합니다</p>
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
              전세가율/갭투자 분석
            </h1>
            <p className="text-lg text-slate-400">전세가율과 갭투자 기회를 분석합니다</p>
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

  if (!jeonseData?.success || !jeonseData?.data || !gapData?.success || !gapData?.data) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              전세가율/갭투자 분석
            </h1>
            <p className="text-lg text-slate-400">전세가율과 갭투자 기회를 분석합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <PiggyBank className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const { by_region, high_ratio_apartments, low_ratio_apartments, jeonse_stats, risk_summary } =
    jeonseData.data;
  const { opportunities, gap_stats } = gapData.data;

  const avgRatioColor =
    jeonse_stats.avg_jeonse_ratio >= 80
      ? "from-red-400 to-rose-400"
      : jeonse_stats.avg_jeonse_ratio >= 70
        ? "from-amber-400 to-orange-400"
        : "from-green-400 to-emerald-400";

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-600/20 via-orange-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-amber-500 to-orange-600 opacity-10 blur-3xl"
          animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute right-1/3 top-40 h-80 w-80 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 opacity-10 blur-3xl"
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
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/10 px-4 py-2">
            <PiggyBank className="h-4 w-4 text-amber-400" />
            <span className="text-sm font-semibold text-amber-300">투자 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-amber-100 to-orange-200 bg-clip-text text-5xl font-bold text-transparent">
            전세가율/갭투자 분석
          </h1>
          <p className="text-xl text-slate-400">전세가율과 갭투자 기회를 분석합니다</p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 space-y-4"
        >
          <RegionFilter value={region} onChange={setRegion} />

          <div className="flex flex-wrap gap-4">
            <div className="min-w-[200px] flex-1">
              <label className="mb-2 block text-sm font-medium text-slate-300">
                최소 전세가율: {minJeonseRatio}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={minJeonseRatio}
                onChange={(e) => setMinJeonseRatio(Number(e.target.value))}
                className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-white/10 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gradient-to-r [&::-webkit-slider-thumb]:from-amber-500 [&::-webkit-slider-thumb]:to-orange-500"
              />
            </div>

            <div className="min-w-[200px] flex-1">
              <label className="mb-2 block text-sm font-medium text-slate-300">
                최소 갭 비율: {minGapRatio}%
              </label>
              <input
                type="range"
                min="0"
                max="50"
                value={minGapRatio}
                onChange={(e) => setMinGapRatio(Number(e.target.value))}
                className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-white/10 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-gradient-to-r [&::-webkit-slider-thumb]:from-green-500 [&::-webkit-slider-thumb]:to-emerald-500"
              />
            </div>
          </div>
        </motion.div>

        {/* Jeonse Analysis Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-16"
        >
          <h2 className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent">
            전세가율 분석
          </h2>

          {/* Stats Cards */}
          <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { title: "평균 전세가율", value: `${jeonse_stats.avg_jeonse_ratio.toFixed(1)}%`, gradient: avgRatioColor, icon: TrendingUp },
              { title: "중앙 전세가율", value: `${jeonse_stats.median_jeonse_ratio.toFixed(1)}%`, gradient: "from-blue-400 to-cyan-400", icon: Target },
              { title: "평균 갭", value: `${Math.round(jeonse_stats.avg_gap / 10000).toLocaleString("ko-KR")}억원`, gradient: "from-purple-400 to-pink-400", icon: DollarSign },
              { title: "매칭된 아파트", value: `${jeonse_stats.matched_apartments.toLocaleString("ko-KR")}개`, gradient: "from-indigo-400 to-violet-400", icon: Shield },
            ].map((stat, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all duration-300 hover:from-white/10"
              >
                <div className={`absolute -inset-1 bg-gradient-to-r ${stat.gradient} opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20`}></div>
                <div className="relative">
                  <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r ${stat.gradient}`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                  <p className="mb-2 text-sm text-slate-400">{stat.title}</p>
                  <p className={`bg-gradient-to-r ${stat.gradient} bg-clip-text text-3xl font-bold text-transparent`}>
                    {stat.value}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Risk Cards */}
          <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-3">
            <div className="overflow-hidden rounded-2xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 p-6 backdrop-blur-sm">
              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-500/20">
                  <AlertTriangle className="h-5 w-5 text-red-400" />
                </div>
                <h3 className="text-lg font-semibold text-red-300">위험 (80% 이상)</h3>
              </div>
              <p className="bg-gradient-to-r from-red-400 to-rose-400 bg-clip-text text-4xl font-bold text-transparent">
                {risk_summary.high_risk_count.toLocaleString("ko-KR")}
              </p>
              <p className="text-sm text-red-400/80">개</p>
            </div>

            <div className="overflow-hidden rounded-2xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-6 backdrop-blur-sm">
              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/20">
                  <AlertTriangle className="h-5 w-5 text-amber-400" />
                </div>
                <h3 className="text-lg font-semibold text-amber-300">주의 (70-80%)</h3>
              </div>
              <p className="bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-4xl font-bold text-transparent">
                {risk_summary.medium_risk_count.toLocaleString("ko-KR")}
              </p>
              <p className="text-sm text-amber-400/80">개</p>
            </div>

            <div className="overflow-hidden rounded-2xl border border-green-500/20 bg-gradient-to-br from-green-500/10 to-emerald-500/5 p-6 backdrop-blur-sm">
              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-500/20">
                  <Shield className="h-5 w-5 text-green-400" />
                </div>
                <h3 className="text-lg font-semibold text-green-300">안전 (70% 미만)</h3>
              </div>
              <p className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-4xl font-bold text-transparent">
                {risk_summary.low_risk_count.toLocaleString("ko-KR")}
              </p>
              <p className="text-sm text-green-400/80">개</p>
            </div>
          </div>

          {/* Chart */}
          {by_region.length > 0 && (
            <div className="mb-8 overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <JeonseRatioChart data={by_region} />
            </div>
          )}

          {/* Tables */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="overflow-hidden rounded-3xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 backdrop-blur-sm">
              <div className="border-b border-red-500/20 p-6">
                <h3 className="flex items-center gap-2 text-lg font-semibold text-red-300">
                  <AlertTriangle className="h-5 w-5" />
                  고위험 아파트 TOP 10
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-red-500/20">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-red-300">
                        아파트
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-red-300">
                        지역
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-red-300">
                        전세가율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-red-300">
                        갭
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-red-500/10">
                    {high_ratio_apartments.slice(0, 10).map((apt, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-red-500/5">
                        <td className="px-4 py-3 text-sm text-white">{apt.apt_name}</td>
                        <td className="px-4 py-3 text-sm text-slate-400">{apt.region}</td>
                        <td className="px-4 py-3 text-right text-sm font-semibold text-red-300">
                          {apt.jeonse_ratio.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {Math.round(apt.gap / 10000).toLocaleString("ko-KR")}억
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="overflow-hidden rounded-3xl border border-green-500/20 bg-gradient-to-br from-green-500/10 to-emerald-500/5 backdrop-blur-sm">
              <div className="border-b border-green-500/20 p-6">
                <h3 className="flex items-center gap-2 text-lg font-semibold text-green-300">
                  <Shield className="h-5 w-5" />
                  저전세가율 TOP 10 (투자 기회)
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead className="border-b border-green-500/20">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-green-300">
                        아파트
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-green-300">
                        지역
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-green-300">
                        전세가율
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-green-300">
                        갭
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-green-500/10">
                    {low_ratio_apartments.slice(0, 10).map((apt, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-green-500/5">
                        <td className="px-4 py-3 text-sm text-white">{apt.apt_name}</td>
                        <td className="px-4 py-3 text-sm text-slate-400">{apt.region}</td>
                        <td className="px-4 py-3 text-right text-sm font-semibold text-green-300">
                          {apt.jeonse_ratio.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {Math.round(apt.gap / 10000).toLocaleString("ko-KR")}억
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Gap Investment Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h2 className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent">
            갭투자 분석
          </h2>

          {/* Stats Cards */}
          <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { title: "평균 갭", value: `${Math.round(gap_stats.avg_gap / 10000).toLocaleString("ko-KR")}억원`, gradient: "from-purple-400 to-pink-400" },
              { title: "중앙 갭", value: `${Math.round(gap_stats.median_gap / 10000).toLocaleString("ko-KR")}억원`, gradient: "from-blue-400 to-cyan-400" },
              { title: "최소 갭", value: `${Math.round(gap_stats.min_gap / 10000).toLocaleString("ko-KR")}억원`, gradient: "from-green-400 to-emerald-400" },
              { title: "분석 대상", value: `${gap_stats.total_count.toLocaleString("ko-KR")}개`, gradient: "from-indigo-400 to-violet-400" },
            ].map((stat, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm"
              >
                <div className={`absolute -inset-1 bg-gradient-to-r ${stat.gradient} opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20`}></div>
                <div className="relative">
                  <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r ${stat.gradient}`}>
                    <DollarSign className="h-6 w-6 text-white" />
                  </div>
                  <p className="mb-2 text-sm text-slate-400">{stat.title}</p>
                  <p className={`bg-gradient-to-r ${stat.gradient} bg-clip-text text-3xl font-bold text-transparent`}>
                    {stat.value}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Scatter Chart */}
          {opportunities.length > 0 && (
            <div className="mb-8 overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
              <GapInvestmentScatter data={opportunities} />
            </div>
          )}

          {/* Opportunities Table */}
          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
            <div className="border-b border-white/10 p-6">
              <h3 className="text-lg font-semibold text-white">갭투자 추천 물건 (예상 ROI 순)</h3>
              <p className="mt-1 text-sm text-slate-400">
                전세가의 연 4% 월세 전환 가정 시 투자금 대비 수익률
              </p>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="border-b border-white/10">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                      아파트
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                      지역
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      예상 ROI
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      갭 금액
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      갭 비율
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                      전세가율
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {opportunities
                    .sort((a, b) => (b.estimated_roi || 0) - (a.estimated_roi || 0))
                    .slice(0, 15)
                    .map((opp, idx) => (
                      <tr key={idx} className="transition-colors hover:bg-white/5">
                        <td className="px-4 py-3 text-sm text-white">{opp.apt_name}</td>
                        <td className="px-4 py-3 text-sm text-slate-400">{opp.region}</td>
                        <td className="px-4 py-3 text-right text-sm font-semibold text-blue-300">
                          {opp.estimated_roi?.toFixed(1)}%
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {Math.round(opp.gap / 10000).toLocaleString("ko-KR")}억
                        </td>
                        <td className="px-4 py-3 text-right text-sm text-white">
                          {opp.gap_ratio.toFixed(1)}%
                        </td>
                        <td
                          className={`px-4 py-3 text-right text-sm font-semibold ${
                            opp.jeonse_ratio >= 80
                              ? "text-red-400"
                              : opp.jeonse_ratio >= 70
                                ? "text-amber-400"
                                : "text-green-400"
                          }`}
                        >
                          {opp.jeonse_ratio.toFixed(1)}%
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
}
