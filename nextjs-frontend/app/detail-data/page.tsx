'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Database, Download, FileText, Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { useDetailData } from '@/hooks/useDetailData';
import { DetailDataFilters as Filters } from '@/types/analysis';
import DetailDataFilters from '@/components/filters/DetailDataFilters';
import DetailDataTable from '@/components/tables/DetailDataTable';
import ExportButtons from '@/components/export/ExportButtons';

export default function DetailDataPage() {
  const [filters, setFilters] = useState<Filters>({
    regions: [],
    transactionTypes: [],
    searchQuery: '',
  });
  const [page, setPage] = useState(1);
  const pageSize = 50;

  const { data, totalCount, totalPages, isLoading, error } = useDetailData(
    filters,
    page,
    pageSize
  );

  if (isLoading) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="relative z-10 container mx-auto px-4 py-12">
          <div className="mb-12">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-4 py-2 backdrop-blur-sm">
              <Database className="h-4 w-4 text-cyan-400" />
              <span className="text-sm font-medium text-cyan-300">상세 데이터</span>
            </div>
            <h1 className="mb-4 bg-gradient-to-r from-cyan-200 via-blue-200 to-indigo-200 bg-clip-text text-5xl font-bold text-transparent">
              상세 거래 데이터
            </h1>
          </div>
          <div className="animate-pulse space-y-6">
            <div className="h-96 rounded-3xl bg-slate-700/50"></div>
            <div className="h-64 rounded-3xl bg-slate-700/50"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="relative z-10 container mx-auto px-4 py-12">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-cyan-200 via-blue-200 to-indigo-200 bg-clip-text text-5xl font-bold text-transparent">
              상세 거래 데이터
            </h1>
          </div>
          <div className="rounded-3xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 p-8 backdrop-blur-sm">
            <div className="mb-4 flex items-center gap-3">
              <FileText className="h-6 w-6 text-red-400" />
              <h3 className="text-xl font-semibold text-red-300">
                데이터를 불러오는 중 오류가 발생했습니다
              </h3>
            </div>
            <p className="text-red-400">
              {error instanceof Error
                ? error.message
                : '알 수 없는 오류가 발생했습니다'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Animated background orbs */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -left-32 top-0 h-96 w-96 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, 50, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="absolute -right-32 top-1/3 h-96 w-96 rounded-full bg-gradient-to-r from-blue-500/20 to-indigo-500/20 blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, -50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12"
        >
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-4 py-2 backdrop-blur-sm">
            <Database className="h-4 w-4 text-cyan-400" />
            <span className="text-sm font-medium text-cyan-300">상세 데이터</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-cyan-200 via-blue-200 to-indigo-200 bg-clip-text text-5xl font-bold text-transparent">
            상세 거래 데이터
          </h1>
          <p className="text-lg text-slate-400">
            아파트 거래 상세 데이터를 조회하고 필터링합니다
          </p>
        </motion.div>

        {/* Search Bar & Export */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8 overflow-hidden rounded-2xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 backdrop-blur-sm"
        >
          <div className="flex flex-col gap-4 md:flex-row">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                value={filters.searchQuery || ''}
                onChange={(e) => {
                  setFilters({ ...filters, searchQuery: e.target.value });
                  setPage(1);
                }}
                placeholder="아파트명 또는 지역으로 검색..."
                className="w-full rounded-xl border border-slate-600/50 bg-slate-800/50 py-3 pl-12 pr-4 text-slate-200 backdrop-blur-sm transition-all placeholder:text-slate-500 hover:border-cyan-500/50 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              />
            </div>
            <ExportButtons filters={filters} data={data} />
          </div>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-6"
        >
          <DetailDataFilters
            filters={filters}
            onChange={(newFilters) => {
              setFilters(newFilters);
              setPage(1);
            }}
          />
        </motion.div>

        {/* Results Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-6 overflow-hidden rounded-2xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 backdrop-blur-sm"
        >
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
            <div>
              <p className="mb-1 text-sm text-slate-400">필터 적용 결과</p>
              <p className="text-3xl font-bold text-slate-100">
                {totalCount.toLocaleString('ko-KR')}건
              </p>
            </div>
            <div className="text-right">
              <p className="mb-1 text-sm text-slate-400">현재 페이지</p>
              <p className="text-2xl font-semibold text-slate-100">
                {page} / {totalPages}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Data Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mb-8 overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm"
        >
          {data.length > 0 ? (
            <DetailDataTable
              data={data}
              currentPage={page}
              totalPages={totalPages}
              totalCount={totalCount}
              onPageChange={setPage}
            />
          ) : (
            <div className="p-16 text-center">
              <div className="mx-auto mb-4 inline-flex rounded-full bg-slate-800/50 p-4">
                <Database className="h-8 w-8 text-slate-500" />
              </div>
              <h3 className="mb-2 text-xl font-medium text-slate-400">
                데이터가 없습니다
              </h3>
              <p className="text-sm text-slate-500">
                필터 조건을 변경하거나 초기화해보세요.
              </p>
            </div>
          )}
        </motion.div>

        {/* Pagination */}
        {data.length > 0 && totalPages > 1 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="flex items-center justify-center gap-2"
          >
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="group flex items-center gap-2 rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-2 text-sm font-medium text-slate-300 backdrop-blur-sm transition-all hover:border-cyan-500/50 hover:bg-slate-700/50 hover:text-cyan-300 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:border-slate-600/50 disabled:hover:bg-slate-800/50 disabled:hover:text-slate-300"
            >
              <ChevronLeft className="h-4 w-4" />
              이전
            </button>

            <div className="flex items-center gap-2">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum;
                if (totalPages <= 5) {
                  pageNum = i + 1;
                } else if (page <= 3) {
                  pageNum = i + 1;
                } else if (page >= totalPages - 2) {
                  pageNum = totalPages - 4 + i;
                } else {
                  pageNum = page - 2 + i;
                }

                return (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    className={`h-10 w-10 rounded-xl text-sm font-medium transition-all ${
                      page === pageNum
                        ? 'border border-cyan-500/50 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 text-cyan-300 shadow-lg'
                        : 'border border-slate-600/50 bg-slate-800/50 text-slate-400 backdrop-blur-sm hover:border-cyan-500/30 hover:bg-slate-700/50 hover:text-cyan-400'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>

            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="group flex items-center gap-2 rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-2 text-sm font-medium text-slate-300 backdrop-blur-sm transition-all hover:border-cyan-500/50 hover:bg-slate-700/50 hover:text-cyan-300 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:border-slate-600/50 disabled:hover:bg-slate-800/50 disabled:hover:text-slate-300"
            >
              다음
              <ChevronRight className="h-4 w-4" />
            </button>
          </motion.div>
        )}

        {/* Export Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-12 overflow-hidden rounded-3xl border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 to-blue-500/5 backdrop-blur-sm"
        >
          <div className="p-8">
            <div className="mb-6 flex items-center gap-3">
              <div className="rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 p-3">
                <Download className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-cyan-300">
                데이터 내보내기 가이드
              </h3>
            </div>
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div className="rounded-2xl border border-cyan-500/10 bg-cyan-500/5 p-6">
                <h4 className="mb-4 text-lg font-semibold text-cyan-300">
                  CSV 내보내기
                </h4>
                <ul className="space-y-3 text-sm text-cyan-400/80">
                  <li className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-cyan-400" />
                    <span>엑셀, 구글 스프레드시트에서 열기 가능</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-cyan-400" />
                    <span>필터링된 데이터만 내보내기</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-cyan-400" />
                    <span>한글 인코딩 자동 설정 (UTF-8)</span>
                  </li>
                </ul>
              </div>
              <div className="rounded-2xl border border-blue-500/10 bg-blue-500/5 p-6">
                <h4 className="mb-4 text-lg font-semibold text-blue-300">
                  PDF 리포트
                </h4>
                <ul className="space-y-3 text-sm text-blue-400/80">
                  <li className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                    <span>프리미엄 회원 전용 기능</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                    <span>통계 요약, 차트 포함</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                    <span>전문 리포트 형식으로 출력</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
