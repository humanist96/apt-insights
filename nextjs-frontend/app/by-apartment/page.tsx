'use client';

import { useState } from 'react';
import { useByApartment } from '@/hooks/useByApartment';
import { ApartmentDataItem } from '@/types/analysis';
import RegionFilter from '@/components/filters/RegionFilter';
import ApartmentTable from '@/components/ApartmentTable';
import ApartmentBarChart from '@/components/charts/ApartmentBarChart';
import ApartmentScatterChart from '@/components/charts/ApartmentScatterChart';
import ApartmentDetailModal from '@/components/ApartmentDetailModal';
import StatsCard from '@/components/stats/StatsCard';

export default function ByApartmentPage() {
  const [region, setRegion] = useState<string>('all');
  const [minCount, setMinCount] = useState<number>(0);
  const [search, setSearch] = useState<string>('');
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
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            아파트별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            아파트 단지별 거래 현황을 분석합니다
          </p>
        </div>

        {/* Loading Skeleton */}
        <div className="animate-pulse space-y-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-64"></div>
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-64"></div>
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded flex-1"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"
              ></div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
          </div>

          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            아파트별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            아파트 단지별 거래 현황을 분석합니다
          </p>
        </div>

        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-900 dark:text-red-300 mb-2">
            데이터를 불러오는 중 오류가 발생했습니다
          </h3>
          <p className="text-red-700 dark:text-red-400">
            {error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다'}
          </p>
        </div>
      </div>
    );
  }

  if (!data?.success || !data?.data) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            아파트별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            아파트 단지별 거래 현황을 분석합니다
          </p>
        </div>

        <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            표시할 데이터가 없습니다
          </p>
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
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          아파트별 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          아파트 단지별 거래 현황을 분석합니다
        </p>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-col md:flex-row gap-4">
        <RegionFilter value={region} onChange={setRegion} />

        <div className="w-full md:w-64">
          <label
            htmlFor="min-count"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            최소 거래 건수
          </label>
          <input
            id="min-count"
            type="number"
            value={minCount}
            onChange={(e) => setMinCount(Math.max(0, parseInt(e.target.value) || 0))}
            min="0"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
          />
        </div>

        <div className="flex-1">
          <label
            htmlFor="search"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            아파트 검색
          </label>
          <input
            id="search"
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="아파트명을 입력하세요"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors placeholder-gray-400 dark:placeholder-gray-500"
          />
        </div>
      </div>

      {/* Stats Cards */}
      {apartments.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="총 아파트 수"
            value={apartments.length.toLocaleString('ko-KR')}
            subtitle="Total Apartments"
          />
          <StatsCard
            title="총 거래 건수"
            value={totalTransactions.toLocaleString('ko-KR')}
            subtitle="Total Transactions"
          />
          <StatsCard
            title="평균 거래 가격"
            value={`${Math.round(avgPrice / 10000).toLocaleString('ko-KR')}억원`}
            subtitle="Average Price"
          />
          <StatsCard
            title="최다 거래 아파트"
            value={`${mostActiveApt.count}건`}
            subtitle={mostActiveApt.apt_name}
          />
        </div>
      )}

      {/* Charts */}
      {apartments.length > 0 ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ApartmentBarChart data={apartments} onBarClick={handleSelectApartment} />
            <ApartmentScatterChart data={apartments} onPointClick={handleSelectApartment} />
          </div>

          {/* Table */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              아파트 목록 ({apartments.length.toLocaleString('ko-KR')}개)
            </h3>
            <ApartmentTable data={apartments} onSelectApartment={handleSelectApartment} />
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            검색 조건에 맞는 아파트가 없습니다
          </p>
        </div>
      )}

      {/* Detail Modal */}
      <ApartmentDetailModal
        apartment={selectedApartment}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
}
