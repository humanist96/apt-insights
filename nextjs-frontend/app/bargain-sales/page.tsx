'use client';

import { useState } from 'react';
import { useBargainSales } from '@/hooks/useBargainSales';
import RegionFilter from '@/components/filters/RegionFilter';
import StatsCard from '@/components/stats/StatsCard';
import BargainSalesScatter from '@/components/charts/BargainSalesScatter';
import BargainDistributionChart from '@/components/charts/BargainDistributionChart';
import BargainSalesTable from '@/components/BargainSalesTable';

export default function BargainSalesPage() {
  const [region, setRegion] = useState<string>('all');
  const [thresholdPct, setThresholdPct] = useState<number>(15);
  const [minTransactionCount, setMinTransactionCount] = useState<number>(2);

  const {
    data: bargainData,
    isLoading,
    error,
  } = useBargainSales({
    regionFilter: region,
    thresholdPct,
    minTransactionCount,
  });

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            급매물 탐지 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
          </p>
        </div>

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
            급매물 탐지 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
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

  if (!bargainData?.success || !bargainData?.data) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            급매물 탐지 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
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

  const { bargain_items, stats, by_region } = bargainData.data;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          급매물 탐지 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          동일 아파트 면적대의 평균가 대비 할인된 거래를 탐지합니다
        </p>
      </div>

      <div className="mb-6 space-y-4">
        <RegionFilter value={region} onChange={setRegion} />

        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-2">
            급매물 탐지 기준
          </h3>
          <p className="text-sm text-blue-700 dark:text-blue-400">
            동일 아파트의 같은 면적대(±5㎡)에서 최근 5건 평균가 대비 {thresholdPct}% 이상 낮은
            거래를 급매물로 판정합니다.
          </p>
        </div>

        <div className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-[250px]">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              할인율 기준: {thresholdPct}%
            </label>
            <input
              type="range"
              min="10"
              max="30"
              step="5"
              value={thresholdPct}
              onChange={(e) => setThresholdPct(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
            <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-1">
              <span>10%</span>
              <span>15%</span>
              <span>20%</span>
              <span>25%</span>
              <span>30%</span>
            </div>
          </div>

          <div className="flex-1 min-w-[250px]">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최소 거래 건수: {minTransactionCount}건
            </label>
            <input
              type="range"
              min="2"
              max="10"
              step="1"
              value={minTransactionCount}
              onChange={(e) => setMinTransactionCount(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
            <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-1">
              <span>2건</span>
              <span>5건</span>
              <span>10건</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="급매물 수"
          value={`${stats.bargain_count.toLocaleString('ko-KR')}건`}
          subtitle="Bargain Count"
          className="text-red-600 dark:text-red-400"
        />
        <StatsCard
          title="평균 할인율"
          value={`${stats.avg_discount.toFixed(1)}%`}
          subtitle="Average Discount"
          className="text-orange-600 dark:text-orange-400"
        />
        <StatsCard
          title="최대 할인율"
          value={`${stats.max_discount.toFixed(1)}%`}
          subtitle="Maximum Discount"
          className="text-amber-600 dark:text-amber-400"
        />
        <StatsCard
          title="총 절감액"
          value={`${Math.round(stats.total_savings / 10000).toLocaleString('ko-KR')}억원`}
          subtitle="Total Savings"
          className="text-blue-600 dark:text-blue-400"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <h3 className="text-sm font-semibold text-red-900 dark:text-red-300 mb-2">
            초특급 급매
          </h3>
          <p className="text-xs text-red-700 dark:text-red-400 mb-2">25% 이상 할인</p>
          <p className="text-2xl font-bold text-red-600 dark:text-red-400">
            {bargain_items.filter((item) => item.discount_pct >= 25).length}건
          </p>
        </div>
        <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-6">
          <h3 className="text-sm font-semibold text-orange-900 dark:text-orange-300 mb-2">
            특급 급매
          </h3>
          <p className="text-xs text-orange-700 dark:text-orange-400 mb-2">20-25% 할인</p>
          <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
            {
              bargain_items.filter(
                (item) => item.discount_pct >= 20 && item.discount_pct < 25
              ).length
            }
            건
          </p>
        </div>
        <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-6">
          <h3 className="text-sm font-semibold text-amber-900 dark:text-amber-300 mb-2">
            일반 급매
          </h3>
          <p className="text-xs text-amber-700 dark:text-amber-400 mb-2">15-20% 할인</p>
          <p className="text-2xl font-bold text-amber-600 dark:text-amber-400">
            {
              bargain_items.filter(
                (item) => item.discount_pct >= 15 && item.discount_pct < 20
              ).length
            }
            건
          </p>
        </div>
        <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg p-6">
          <h3 className="text-sm font-semibold text-emerald-900 dark:text-emerald-300 mb-2">
            경미 할인
          </h3>
          <p className="text-xs text-emerald-700 dark:text-emerald-400 mb-2">15% 미만 할인</p>
          <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
            {bargain_items.filter((item) => item.discount_pct < 15).length}건
          </p>
        </div>
      </div>

      {by_region.length > 0 && (
        <div className="mb-8">
          <BargainDistributionChart data={by_region} />
        </div>
      )}

      {bargain_items.length > 0 && (
        <div className="mb-8">
          <BargainSalesScatter data={bargain_items} />
        </div>
      )}

      {bargain_items.length > 0 && <BargainSalesTable data={bargain_items} />}

      {bargain_items.length === 0 && (
        <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            선택한 조건에 해당하는 급매물이 없습니다.
          </p>
          <p className="text-gray-500 dark:text-gray-500 text-sm mt-2">
            할인율 기준을 낮추거나 다른 지역을 선택해 보세요.
          </p>
        </div>
      )}
    </div>
  );
}
