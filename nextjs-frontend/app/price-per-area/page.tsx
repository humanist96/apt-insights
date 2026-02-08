'use client';

import { useState } from 'react';
import { usePricePerArea } from '@/hooks/usePricePerArea';
import { usePricePerAreaTrend } from '@/hooks/usePricePerAreaTrend';
import RegionFilter from '@/components/filters/RegionFilter';
import StatsCard from '@/components/stats/StatsCard';
import PricePerAreaBarChart from '@/components/charts/PricePerAreaBarChart';
import PricePerAreaBoxPlot from '@/components/charts/PricePerAreaBoxPlot';
import PricePerAreaTrendChart from '@/components/charts/PricePerAreaTrendChart';

export default function PricePerAreaPage() {
  const [region, setRegion] = useState<string>('all');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');

  const { data, isLoading, error } = usePricePerArea({
    regionFilter: region !== 'all' ? region : undefined,
    startDate,
    endDate,
  });

  const {
    data: trendData,
    isLoading: trendLoading,
    error: trendError,
  } = usePricePerAreaTrend({
    regionFilter: region !== 'all' ? region : undefined,
    startDate,
    endDate,
  });

  if (isLoading || trendLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            평당가 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            면적당 가격을 분석하여 투자 가치를 평가합니다
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

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
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

  if (error || trendError) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            평당가 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            면적당 가격을 분석하여 투자 가치를 평가합니다
          </p>
        </div>

        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-900 dark:text-red-300 mb-2">
            데이터를 불러오는 중 오류가 발생했습니다
          </h3>
          <p className="text-red-700 dark:text-red-400">
            {error instanceof Error
              ? error.message
              : trendError instanceof Error
              ? trendError.message
              : '알 수 없는 오류가 발생했습니다'}
          </p>
        </div>
      </div>
    );
  }

  if (!data?.success || !data?.data || !trendData?.success || !trendData?.data) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            평당가 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            면적당 가격을 분석하여 투자 가치를 평가합니다
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

  const { stats, by_region, by_area_range, top_expensive, top_affordable } = data.data;
  const { trend } = trendData.data;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          평당가 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          면적당 가격을 분석하여 투자 가치를 평가합니다
        </p>
      </div>

      <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
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
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
          평당가 분석
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="평균 평당가"
            value={`${Math.round(stats.avg_price_per_area).toLocaleString('ko-KR')}만원/㎡`}
            subtitle="Average Price per Area"
          />
          <StatsCard
            title="중앙 평당가"
            value={`${Math.round(stats.median_price_per_area).toLocaleString('ko-KR')}만원/㎡`}
            subtitle="Median Price per Area"
          />
          <StatsCard
            title="최고 평당가"
            value={`${Math.round(stats.max_price_per_area).toLocaleString('ko-KR')}만원/㎡`}
            subtitle="Maximum Price per Area"
          />
          <StatsCard
            title="최저 평당가"
            value={`${Math.round(stats.min_price_per_area).toLocaleString('ko-KR')}만원/㎡`}
            subtitle="Minimum Price per Area"
          />
        </div>

        {by_area_range.length > 0 && by_region.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <PricePerAreaBarChart data={by_area_range} />
            <PricePerAreaBoxPlot data={by_region} />
          </div>
        )}

        {(top_expensive.length > 0 || top_affordable.length > 0) && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
              평당가 상위 아파트
            </h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {top_expensive.length > 0 && (
                <div>
                  <h4 className="text-md font-semibold text-gray-800 dark:text-gray-200 mb-4">
                    최고가 TOP 10
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                      <thead className="bg-gray-50 dark:bg-gray-900">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                            아파트
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                            평당가
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                            면적
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                        {top_expensive.map((item, index) => (
                          <tr key={index}>
                            <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                              <div>{item.apt_name}</div>
                              <div className="text-xs text-gray-500 dark:text-gray-400">
                                {item.region}
                              </div>
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-700 dark:text-gray-300">
                              {Math.round(item.price_per_area).toLocaleString('ko-KR')}
                              만원/㎡
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-700 dark:text-gray-300">
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
                  <h4 className="text-md font-semibold text-gray-800 dark:text-gray-200 mb-4">
                    최저가 TOP 10
                  </h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                      <thead className="bg-gray-50 dark:bg-gray-900">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                            아파트
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                            평당가
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                            면적
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                        {top_affordable.map((item, index) => (
                          <tr key={index}>
                            <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                              <div>{item.apt_name}</div>
                              <div className="text-xs text-gray-500 dark:text-gray-400">
                                {item.region}
                              </div>
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-700 dark:text-gray-300">
                              {Math.round(item.price_per_area).toLocaleString('ko-KR')}
                              만원/㎡
                            </td>
                            <td className="px-4 py-3 text-sm text-right text-gray-700 dark:text-gray-300">
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
          </div>
        )}
      </div>

      {trend.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            평당가 추이
          </h2>

          <div className="mb-6">
            <PricePerAreaTrendChart data={trend} />
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              월별 평당가 통계
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-900">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      년월
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      평균 평당가
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      중앙 평당가
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      거래 건수
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      변동률
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {trend.map((item) => (
                    <tr key={item.year_month}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        {item.year_month}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {Math.round(item.avg_price_per_area).toLocaleString('ko-KR')}
                        만원/㎡
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {Math.round(item.median_price_per_area).toLocaleString('ko-KR')}
                        만원/㎡
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                        {item.count.toLocaleString('ko-KR')}건
                      </td>
                      <td
                        className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                          item.change_rate && item.change_rate > 0
                            ? 'text-red-600 dark:text-red-400'
                            : item.change_rate && item.change_rate < 0
                            ? 'text-blue-600 dark:text-blue-400'
                            : 'text-gray-700 dark:text-gray-300'
                        }`}
                      >
                        {item.change_rate
                          ? `${item.change_rate > 0 ? '+' : ''}${item.change_rate.toFixed(2)}%`
                          : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
