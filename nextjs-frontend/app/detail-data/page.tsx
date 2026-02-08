'use client';

import { useState } from 'react';
import { useDetailData } from '@/hooks/useDetailData';
import { DetailDataFilters as Filters } from '@/types/analysis';
import DetailDataFilters from '@/components/filters/DetailDataFilters';
import DetailDataTable from '@/components/tables/DetailDataTable';
import ExportButtons from '@/components/export/ExportButtons';
import Card from '@/components/ui/Card';

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
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            상세 데이터
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            아파트 거래 상세 데이터를 조회하고 필터링합니다
          </p>
        </div>

        <div className="animate-pulse space-y-6">
          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
          <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            상세 데이터
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            아파트 거래 상세 데이터를 조회하고 필터링합니다
          </p>
        </div>

        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-900 dark:text-red-300 mb-2">
            데이터를 불러오는 중 오류가 발생했습니다
          </h3>
          <p className="text-red-700 dark:text-red-400">
            {error instanceof Error
              ? error.message
              : '알 수 없는 오류가 발생했습니다'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          상세 데이터
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          아파트 거래 상세 데이터를 조회하고 필터링합니다
        </p>
      </div>

      {/* Search Bar */}
      <Card className="mb-6">
        <div className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={filters.searchQuery || ''}
              onChange={(e) => {
                setFilters({ ...filters, searchQuery: e.target.value });
                setPage(1);
              }}
              placeholder="아파트명 또는 지역으로 검색..."
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <ExportButtons filters={filters} data={data} />
        </div>
      </Card>

      {/* Filters */}
      <DetailDataFilters
        filters={filters}
        onChange={(newFilters) => {
          setFilters(newFilters);
          setPage(1);
        }}
      />

      {/* Results Summary */}
      <div className="mb-4">
        <Card>
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                필터 적용 결과
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {totalCount.toLocaleString('ko-KR')}건
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                현재 페이지
              </p>
              <p className="text-xl font-semibold text-gray-900 dark:text-white">
                {page} / {totalPages}
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Data Table */}
      {data.length > 0 ? (
        <DetailDataTable
          data={data}
          currentPage={page}
          totalPages={totalPages}
          totalCount={totalCount}
          onPageChange={setPage}
        />
      ) : (
        <Card>
          <div className="py-12 text-center">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
              데이터가 없습니다
            </h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              필터 조건을 변경하거나 초기화해보세요.
            </p>
          </div>
        </Card>
      )}
    </div>
  );
}
