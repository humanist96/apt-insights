'use client';

import { useState } from 'react';
import { useJeonseAnalysis } from '@/hooks/useJeonseAnalysis';
import { useGapInvestment } from '@/hooks/useGapInvestment';
import RegionFilter from '@/components/filters/RegionFilter';
import StatsCard from '@/components/stats/StatsCard';
import JeonseRatioChart from '@/components/charts/JeonseRatioChart';
import GapInvestmentScatter from '@/components/charts/GapInvestmentScatter';

export default function InvestmentPage() {
  const [region, setRegion] = useState<string>('all');
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
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            전세가율/갭투자 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            전세가율과 갭투자 기회를 분석합니다
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
            전세가율/갭투자 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            전세가율과 갭투자 기회를 분석합니다
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

  if (!jeonseData?.success || !jeonseData?.data || !gapData?.success || !gapData?.data) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            전세가율/갭투자 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            전세가율과 갭투자 기회를 분석합니다
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

  const { by_region, high_ratio_apartments, low_ratio_apartments, jeonse_stats, risk_summary } =
    jeonseData.data;
  const { opportunities, gap_stats, by_gap_range } = gapData.data;

  const avgRatioColor =
    jeonse_stats.avg_jeonse_ratio >= 80
      ? 'text-red-600 dark:text-red-400'
      : jeonse_stats.avg_jeonse_ratio >= 70
      ? 'text-yellow-600 dark:text-yellow-400'
      : 'text-green-600 dark:text-green-400';

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          전세가율/갭투자 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          전세가율과 갭투자 기회를 분석합니다
        </p>
      </div>

      <div className="mb-6 space-y-4">
        <RegionFilter value={region} onChange={setRegion} />

        <div className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최소 전세가율: {minJeonseRatio}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={minJeonseRatio}
              onChange={(e) => setMinJeonseRatio(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
          </div>

          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최소 갭 비율: {minGapRatio}%
            </label>
            <input
              type="range"
              min="0"
              max="50"
              value={minGapRatio}
              onChange={(e) => setMinGapRatio(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
          </div>
        </div>
      </div>

      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          전세가율 분석
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="평균 전세가율"
            value={`${jeonse_stats.avg_jeonse_ratio.toFixed(1)}%`}
            subtitle="Average Jeonse Ratio"
            className={avgRatioColor}
          />
          <StatsCard
            title="중앙 전세가율"
            value={`${jeonse_stats.median_jeonse_ratio.toFixed(1)}%`}
            subtitle="Median Jeonse Ratio"
          />
          <StatsCard
            title="평균 갭"
            value={`${Math.round(jeonse_stats.avg_gap / 10000).toLocaleString('ko-KR')}억원`}
            subtitle="Average Gap"
          />
          <StatsCard
            title="매칭된 아파트"
            value={`${jeonse_stats.matched_apartments.toLocaleString('ko-KR')}개`}
            subtitle="Matched Apartments"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-red-900 dark:text-red-300 mb-2">
              위험 (80% 이상)
            </h3>
            <p className="text-3xl font-bold text-red-600 dark:text-red-400">
              {risk_summary.high_risk_count.toLocaleString('ko-KR')}개
            </p>
          </div>
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-300 mb-2">
              주의 (70-80%)
            </h3>
            <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">
              {risk_summary.medium_risk_count.toLocaleString('ko-KR')}개
            </p>
          </div>
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-green-900 dark:text-green-300 mb-2">
              안전 (70% 미만)
            </h3>
            <p className="text-3xl font-bold text-green-600 dark:text-green-400">
              {risk_summary.low_risk_count.toLocaleString('ko-KR')}개
            </p>
          </div>
        </div>

        {by_region.length > 0 && (
          <div className="mb-8">
            <JeonseRatioChart data={by_region} />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-red-900 dark:text-red-300 mb-4">
              고위험 아파트 TOP 10 (전세가율 높은 순)
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      아파트
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      지역
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      전세가율
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      갭
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {high_ratio_apartments.slice(0, 10).map((apt, idx) => (
                    <tr key={idx}>
                      <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        {apt.apt_name}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                        {apt.region}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-red-600 dark:text-red-400 font-semibold">
                        {apt.jeonse_ratio.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                        {Math.round(apt.gap / 10000).toLocaleString('ko-KR')}억
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-green-900 dark:text-green-300 mb-4">
              저전세가율 아파트 TOP 10 (투자 기회)
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      아파트
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      지역
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      전세가율
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                      갭
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {low_ratio_apartments.slice(0, 10).map((apt, idx) => (
                    <tr key={idx}>
                      <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        {apt.apt_name}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                        {apt.region}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-green-600 dark:text-green-400 font-semibold">
                        {apt.jeonse_ratio.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                        {Math.round(apt.gap / 10000).toLocaleString('ko-KR')}억
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          갭투자 분석
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="평균 갭"
            value={`${Math.round(gap_stats.avg_gap / 10000).toLocaleString('ko-KR')}억원`}
            subtitle="Average Gap"
          />
          <StatsCard
            title="중앙 갭"
            value={`${Math.round(gap_stats.median_gap / 10000).toLocaleString('ko-KR')}억원`}
            subtitle="Median Gap"
          />
          <StatsCard
            title="최소 갭"
            value={`${Math.round(gap_stats.min_gap / 10000).toLocaleString('ko-KR')}억원`}
            subtitle="Minimum Gap"
          />
          <StatsCard
            title="분석 대상"
            value={`${gap_stats.total_count.toLocaleString('ko-KR')}개`}
            subtitle="Total Count"
          />
        </div>

        {opportunities.length > 0 && (
          <div className="mb-8">
            <GapInvestmentScatter data={opportunities} />
          </div>
        )}

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            갭투자 추천 물건 (예상 ROI 순)
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            전세가의 연 4% 월세 전환 가정 시 투자금 대비 수익률
          </p>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    아파트
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    지역
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    예상 ROI
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    갭 금액
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    갭 비율
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    전세가율
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {opportunities
                  .sort((a, b) => (b.estimated_roi || 0) - (a.estimated_roi || 0))
                  .slice(0, 15)
                  .map((opp, idx) => (
                    <tr key={idx}>
                      <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        {opp.apt_name}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                        {opp.region}
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-blue-600 dark:text-blue-400 font-semibold">
                        {opp.estimated_roi?.toFixed(1)}%
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                        {Math.round(opp.gap / 10000).toLocaleString('ko-KR')}억
                      </td>
                      <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                        {opp.gap_ratio.toFixed(1)}%
                      </td>
                      <td
                        className={`px-4 py-3 text-sm text-right font-semibold ${
                          opp.jeonse_ratio >= 80
                            ? 'text-red-600 dark:text-red-400'
                            : opp.jeonse_ratio >= 70
                            ? 'text-yellow-600 dark:text-yellow-400'
                            : 'text-green-600 dark:text-green-400'
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
      </section>
    </div>
  );
}
