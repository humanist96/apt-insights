"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useByApartment } from "@/hooks/useByApartment";
import { ApartmentDataItem } from "@/types/analysis";
import RegionFilter from "@/components/filters/RegionFilter";
import ApartmentTable from "@/components/ApartmentTable";
import ApartmentBarChart from "@/components/charts/ApartmentBarChart";
import ApartmentScatterChart from "@/components/charts/ApartmentScatterChart";
import ApartmentDetailModal from "@/components/ApartmentDetailModal";
import StatsCard from "@/components/stats/StatsCard";
import { Building2, Search, BarChart3, TrendingUp, AlertCircle } from "lucide-react";

export default function ByApartmentPage() {
  const [region, setRegion] = useState<string>("all");
  const [minCount, setMinCount] = useState<number>(0);
  const [search, setSearch] = useState<string>("");
  const [selectedApartment, setSelectedApartment] = useState<ApartmentDataItem | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { data, isLoading, error } = useByApartment({ region, minCount, search });

  const handleSelectApartment = (apartment: ApartmentDataItem) => {
    setSelectedApartment(apartment);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedApartment(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute left-1/3 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 opacity-10 blur-3xl"
            animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>

        <div className="container relative mx-auto px-4 py-16">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent">
              아파트별 분석
            </h1>
            <p className="text-lg text-slate-400">아파트 단지별 거래 현황을 분석합니다</p>
          </div>

          <div className="space-y-8 animate-pulse">
            <div className="flex flex-col gap-4 md:flex-row">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-12 rounded-xl bg-white/5 border border-white/10 flex-1"></div>
              ))}
            </div>

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
              아파트별 분석
            </h1>
            <p className="text-lg text-slate-400">아파트 단지별 거래 현황을 분석합니다</p>
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
              아파트별 분석
            </h1>
            <p className="text-lg text-slate-400">아파트 단지별 거래 현황을 분석합니다</p>
          </div>

          <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-white/5">
              <Building2 className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const apartments = data.data.data;

  const totalTransactions = apartments.reduce((sum, apt) => sum + apt.count, 0);
  const avgPrice =
    apartments.reduce((sum, apt) => sum + (apt.avg_price || 0), 0) / apartments.length;
  const highestPriceApt = apartments.reduce((prev, curr) =>
    (curr.avg_price || 0) > (prev.avg_price || 0) ? curr : prev
  );
  const mostActiveApt = apartments.reduce((prev, curr) =>
    curr.count > prev.count ? curr : prev
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-green-600/20 via-emerald-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/3 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-green-500 to-emerald-600 opacity-10 blur-3xl"
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
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/10 px-4 py-2">
            <Building2 className="h-4 w-4 text-green-400" />
            <span className="text-sm font-semibold text-green-300">아파트 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-green-100 to-emerald-200 bg-clip-text text-5xl font-bold text-transparent">
            아파트별 분석
          </h1>
          <p className="text-xl text-slate-400">아파트 단지별 거래 현황을 분석합니다</p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 flex flex-col gap-4 md:flex-row"
        >
          <div className="w-full md:w-64">
            <label htmlFor="region-filter" className="mb-2 block text-sm font-medium text-slate-300">
              지역 선택
            </label>
            <RegionFilter value={region} onChange={setRegion} />
          </div>

          <div className="w-full md:w-64">
            <label htmlFor="min-count" className="mb-2 block text-sm font-medium text-slate-300">
              최소 거래 건수
            </label>
            <input
              id="min-count"
              type="number"
              value={minCount}
              onChange={(e) => setMinCount(Math.max(0, parseInt(e.target.value) || 0))}
              min="0"
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-white backdrop-blur-sm transition-all focus:border-green-500/50 focus:outline-none focus:ring-2 focus:ring-green-500/50"
            />
          </div>

          <div className="flex-1">
            <label htmlFor="search" className="mb-2 block text-sm font-medium text-slate-300">
              아파트 검색
            </label>
            <div className="relative">
              <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                <Search className="h-5 w-5 text-slate-400" />
              </div>
              <input
                id="search"
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="아파트명을 입력하세요"
                className="w-full rounded-xl border border-white/10 bg-white/5 py-3 pl-12 pr-4 text-white placeholder-slate-500 backdrop-blur-sm transition-all focus:border-green-500/50 focus:outline-none focus:ring-2 focus:ring-green-500/50"
              />
            </div>
          </div>
        </motion.div>

        {/* Stats Cards */}
        {apartments.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4"
          >
            <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-green-500/30">
              <div className="absolute -inset-1 bg-gradient-to-r from-green-500 to-emerald-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
              <div className="relative">
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-green-500 to-emerald-500">
                  <Building2 className="h-6 w-6 text-white" />
                </div>
                <p className="mb-2 text-sm text-slate-400">총 아파트 수</p>
                <p className="mb-1 bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-3xl font-bold text-transparent">
                  {apartments.length.toLocaleString("ko-KR")}
                </p>
                <p className="text-xs text-slate-500">Total Apartments</p>
              </div>
            </div>

            <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-blue-500/30">
              <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-cyan-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
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

            <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-purple-500/30">
              <div className="absolute -inset-1 bg-gradient-to-r from-purple-500 to-pink-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
              <div className="relative">
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-purple-500 to-pink-500">
                  <TrendingUp className="h-6 w-6 text-white" />
                </div>
                <p className="mb-2 text-sm text-slate-400">평균 거래 가격</p>
                <p className="mb-1 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-3xl font-bold text-transparent">
                  {Math.round(avgPrice / 10000).toLocaleString("ko-KR")}억원
                </p>
                <p className="text-xs text-slate-500">Average Price</p>
              </div>
            </div>

            <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm transition-all hover:border-amber-500/30">
              <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 to-orange-500 opacity-0 blur-xl transition-opacity group-hover:opacity-20"></div>
              <div className="relative">
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-amber-500 to-orange-500">
                  <BarChart3 className="h-6 w-6 text-white" />
                </div>
                <p className="mb-2 text-sm text-slate-400">최다 거래 아파트</p>
                <p className="mb-1 bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-3xl font-bold text-transparent">
                  {mostActiveApt.count}건
                </p>
                <p className="text-xs text-slate-500">{mostActiveApt.apt_name}</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Charts and Table */}
        {apartments.length > 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <ApartmentBarChart data={apartments} onBarClick={handleSelectApartment} />
              </div>
              <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-6 backdrop-blur-sm">
                <ApartmentScatterChart data={apartments} onPointClick={handleSelectApartment} />
              </div>
            </div>

            <div className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm">
              <div className="p-6">
                <h3 className="mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-2xl font-bold text-transparent">
                  아파트 목록 ({apartments.length.toLocaleString("ko-KR")}개)
                </h3>
                <ApartmentTable data={apartments} onSelectApartment={handleSelectApartment} />
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
              <Building2 className="h-8 w-8 text-slate-400" />
            </div>
            <p className="text-lg text-slate-400">검색 조건에 맞는 아파트가 없습니다</p>
          </motion.div>
        )}

        {/* Detail Modal */}
        <ApartmentDetailModal
          apartment={selectedApartment}
          isOpen={isModalOpen}
          onClose={handleCloseModal}
        />
      </div>
    </div>
  );
}
