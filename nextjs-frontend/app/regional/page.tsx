'use client';

import { useState } from 'react';
import { useRegionalAnalysis } from '@/hooks/useRegionalAnalysis';
import RegionFilter from '@/components/filters/RegionFilter';
import RegionalBarChart from '@/components/charts/RegionalBarChart';
import RegionalPieChart from '@/components/charts/RegionalPieChart';
import StatsCard from '@/components/stats/StatsCard';

export default function RegionalPage() {
  const [region, setRegion] = useState<string>('all');
  const { data, isLoading, error } = useRegionalAnalysis(region);

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            지역별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            지역별 아파트 거래 현황을 분석합니다
          </p>
        </div>

        {/* Loading Skeleton */}
        <div className="animate-pulse space-y-6">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-64"></div>

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
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            지역별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            지역별 아파트 거래 현황을 분석합니다
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
            지역별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            지역별 아파트 거래 현황을 분석합니다
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

  const { by_region, summary } = data.data;

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          지역별 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          지역별 아파트 거래 현황을 분석합니다
        </p>
      </div>

      {/* Filter */}
      <div className="mb-6">
        <RegionFilter value={region} onChange={setRegion} />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="총 거래 건수"
          value={summary.total_transactions.toLocaleString('ko-KR')}
          subtitle="Total Transactions"
        />
        <StatsCard
          title="평균 거래 가격"
          value={`${Math.round(summary.average_price / 10000).toLocaleString('ko-KR')}억원`}
          subtitle="Average Price"
        />
        <StatsCard
          title="최고가 지역"
          value={
            summary.highest_region
              ? `${Math.round(summary.highest_region.avg_price / 10000).toLocaleString('ko-KR')}억원`
              : '-'
          }
          subtitle={summary.highest_region?.region || 'N/A'}
        />
        <StatsCard
          title="최저가 지역"
          value={
            summary.lowest_region
              ? `${Math.round(summary.lowest_region.avg_price / 10000).toLocaleString('ko-KR')}억원`
              : '-'
          }
          subtitle={summary.lowest_region?.region || 'N/A'}
        />
      </div>

      {/* Charts */}
      {by_region.length > 0 ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RegionalBarChart data={by_region} />
          <RegionalPieChart data={by_region} />
        </div>
      ) : (
        <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            선택한 지역에 대한 데이터가 없습니다
          </p>
        </div>
      )}
    </div>
  );
}
