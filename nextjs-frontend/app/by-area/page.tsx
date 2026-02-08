'use client';

import { useState } from 'react';
import { useByArea } from '@/hooks/useByArea';
import RegionFilter from '@/components/filters/RegionFilter';
import AreaBinsSelector from '@/components/AreaBinsSelector';
import StatsCard from '@/components/stats/StatsCard';
import AreaDistributionChart from '@/components/charts/AreaDistributionChart';
import AreaPriceChart from '@/components/charts/AreaPriceChart';
import AreaPricePerAreaChart from '@/components/charts/AreaPricePerAreaChart';

const DEFAULT_BINS = [50, 60, 85, 100, 135];

export default function ByAreaPage() {
  const [region, setRegion] = useState<string>('all');
  const [bins, setBins] = useState<number[]>(DEFAULT_BINS);

  const { data, isLoading, error } = useByArea({ region, bins });

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            면적별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            전용면적에 따른 거래 현황을 분석합니다
          </p>
        </div>

        <div className="animate-pulse space-y-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-64"></div>
          </div>

          <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2].map((i) => (
              <div
                key={i}
                className="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"
              ></div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg"
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
            면적별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            전용면적에 따른 거래 현황을 분석합니다
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
            면적별 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            전용면적에 따른 거래 현황을 분석합니다
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

  const areaData = data.data.data;
  const summary = data.data.summary;

  const totalTransactions = summary.total_transactions;
  const mostCommonRange = summary.most_common_range;
  const avgPriceAcrossAll = areaData.length > 0
    ? areaData.reduce((sum, item) => sum + item.avg_price, 0) / areaData.length
    : 0;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          면적별 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          전용면적에 따른 거래 현황을 분석합니다
        </p>
      </div>

      <div className="mb-6 flex flex-col gap-4">
        <RegionFilter value={region} onChange={setRegion} />

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <AreaBinsSelector bins={bins} onChange={setBins} />
        </div>
      </div>

      {areaData.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
          <StatsCard
            title="총 거래 건수"
            value={totalTransactions.toLocaleString('ko-KR')}
            subtitle="Total Transactions"
          />
          <StatsCard
            title="가장 많은 거래 면적대"
            value={mostCommonRange ? mostCommonRange.area_range.replace('~', '-') + '㎡' : 'N/A'}
            subtitle={mostCommonRange ? `${mostCommonRange.count.toLocaleString('ko-KR')}건` : ''}
          />
        </div>
      )}

      {areaData.length > 0 ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AreaDistributionChart data={areaData} />
            <AreaPriceChart data={areaData} />
          </div>

          <AreaPricePerAreaChart data={areaData} />

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                면적대별 상세 통계
              </h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-900">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      면적구간 (㎡)
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      거래건수
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      평균가격 (억원)
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      중앙가격 (억원)
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      최고가격 (억원)
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      최저가격 (억원)
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      평균면적 (㎡)
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      ㎡당 가격 (만원)
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {areaData.map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                        {item.area_range.replace('~', ' - ')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {item.count.toLocaleString('ko-KR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {Math.round(item.avg_price / 10000).toLocaleString('ko-KR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {Math.round(item.median_price / 10000).toLocaleString('ko-KR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {item.max_price ? Math.round(item.max_price / 10000).toLocaleString('ko-KR') : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {item.min_price ? Math.round(item.min_price / 10000).toLocaleString('ko-KR') : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {item.avg_area.toFixed(1)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white">
                        {Math.round(item.price_per_area).toLocaleString('ko-KR')}
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
            선택한 조건에 맞는 데이터가 없습니다
          </p>
        </div>
      )}
    </div>
  );
}
