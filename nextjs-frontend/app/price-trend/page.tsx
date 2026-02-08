'use client';

import { useState } from 'react';
import { usePriceTrend } from '@/hooks/usePriceTrend';
import PriceTrendLineChart from '@/components/charts/PriceTrendLineChart';
import TransactionVolumeChart from '@/components/charts/TransactionVolumeChart';
import CombinedPriceVolumeChart from '@/components/charts/CombinedPriceVolumeChart';
import StatsCard from '@/components/stats/StatsCard';
import RegionFilter from '@/components/filters/RegionFilter';

export default function PriceTrendPage() {
  const [region, setRegion] = useState<string>('all');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [groupBy, setGroupBy] = useState<'month' | 'quarter'>('month');

  const { data, isLoading, error } = usePriceTrend({
    startDate,
    endDate,
    regionFilter: region !== 'all' ? region : undefined,
    groupBy,
  });

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            가격 추이 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            시간에 따른 아파트 가격 변동을 분석합니다
          </p>
        </div>

        <div className="animate-pulse space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"
              ></div>
            ))}
          </div>

          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>

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
            가격 추이 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            시간에 따른 아파트 가격 변동을 분석합니다
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

  if (!data?.success || !data?.data) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            가격 추이 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            시간에 따른 아파트 가격 변동을 분석합니다
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

  const { trend_data, summary } = data.data;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          가격 추이 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          시간에 따른 아파트 가격 변동을 분석합니다
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label
            htmlFor="region-filter"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            지역 선택
          </label>
          <RegionFilter value={region} onChange={setRegion} />
        </div>

        <div>
          <label
            htmlFor="start-date"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            시작일
          </label>
          <input
            type="month"
            id="start-date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label
            htmlFor="end-date"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            종료일
          </label>
          <input
            type="month"
            id="end-date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label
            htmlFor="group-by"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            집계 단위
          </label>
          <select
            id="group-by"
            value={groupBy}
            onChange={(e) => setGroupBy(e.target.value as 'month' | 'quarter')}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="month">월별</option>
            <option value="quarter">분기별</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="총 기간"
          value={`${summary.total_months}개월`}
          subtitle="Total Months"
        />
        <StatsCard
          title="전체 평균 가격"
          value={`${Math.round(summary.overall_avg_price / 10000).toLocaleString('ko-KR')}억원`}
          subtitle="Overall Average Price"
        />
        <StatsCard
          title="가격 변동률"
          value={`${summary.price_change_pct > 0 ? '+' : ''}${summary.price_change_pct.toFixed(1)}%`}
          subtitle="Price Change"
        />
        <StatsCard
          title="총 거래 건수"
          value={summary.total_transactions.toLocaleString('ko-KR')}
          subtitle="Total Transactions"
        />
      </div>

      {trend_data.length > 0 ? (
        <div className="space-y-6">
          <PriceTrendLineChart data={trend_data} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <TransactionVolumeChart data={trend_data} />
            <CombinedPriceVolumeChart data={trend_data} />
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              월별 통계 테이블
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-900">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      년월
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      평균 가격
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      중앙 가격
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      거래 건수
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      최고가
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      최저가
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {trend_data.map((item) => (
                    <tr key={item.year_month}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        {item.year_month}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {Math.round(item.avg_price / 10000).toLocaleString(
                          'ko-KR'
                        )}
                        억원
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {Math.round(item.median_price / 10000).toLocaleString(
                          'ko-KR'
                        )}
                        억원
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {item.count.toLocaleString('ko-KR')}건
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {Math.round(item.max_price / 10000).toLocaleString(
                          'ko-KR'
                        )}
                        억원
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {Math.round(item.min_price / 10000).toLocaleString(
                          'ko-KR'
                        )}
                        억원
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center">
          <p className="text-gray-600 dark:text-gray-400 text-lg">
            선택한 기간에 대한 데이터가 없습니다
          </p>
        </div>
      )}
    </div>
  );
}
