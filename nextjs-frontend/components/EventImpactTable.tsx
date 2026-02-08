'use client';

import { EventImpact } from '@/types/analysis';

interface EventImpactTableProps {
  impacts: EventImpact[];
}

export default function EventImpactTable({ impacts }: EventImpactTableProps) {
  if (impacts.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          이벤트 영향 분석
        </h3>
        <p className="text-gray-500 dark:text-gray-400 text-center py-8">
          이벤트가 없거나 분석할 데이터가 부족합니다
        </p>
      </div>
    );
  }

  const sortedImpacts = [...impacts].sort(
    (a, b) => new Date(b.event.date).getTime() - new Date(a.event.date).getTime()
  );

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        이벤트 영향 분석
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        각 이벤트 전후 ±30일 데이터를 비교합니다
      </p>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-900">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                이벤트
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                날짜
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                이전 평균가격
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                이후 평균가격
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                가격 변동
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                거래량 변동
              </th>
              <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                유의미성
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {sortedImpacts.map((impact) => {
              const priceChangeColor =
                impact.price_change_pct > 0
                  ? 'text-green-600 dark:text-green-400'
                  : impact.price_change_pct < 0
                    ? 'text-red-600 dark:text-red-400'
                    : 'text-gray-600 dark:text-gray-400';

              const volumeChangeColor =
                impact.volume_change_pct > 0
                  ? 'text-green-600 dark:text-green-400'
                  : impact.volume_change_pct < 0
                    ? 'text-red-600 dark:text-red-400'
                    : 'text-gray-600 dark:text-gray-400';

              return (
                <tr key={impact.event.id} className="hover:bg-gray-50 dark:hover:bg-gray-900/50">
                  <td className="px-4 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {impact.event.name}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {impact.event.type}
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                    {new Date(impact.event.date).toLocaleDateString('ko-KR', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                    {impact.before.avg_price > 0
                      ? `${Math.round(impact.before.avg_price / 10000).toLocaleString('ko-KR')}억원`
                      : 'N/A'}
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {impact.before.count}건
                    </div>
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                    {impact.after.avg_price > 0
                      ? `${Math.round(impact.after.avg_price / 10000).toLocaleString('ko-KR')}억원`
                      : 'N/A'}
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {impact.after.count}건
                    </div>
                  </td>
                  <td
                    className={`px-4 py-4 whitespace-nowrap text-sm text-right font-semibold ${priceChangeColor}`}
                  >
                    {impact.before.avg_price > 0 && impact.after.avg_price > 0
                      ? `${impact.price_change_pct > 0 ? '+' : ''}${impact.price_change_pct.toFixed(1)}%`
                      : 'N/A'}
                  </td>
                  <td
                    className={`px-4 py-4 whitespace-nowrap text-sm text-right font-semibold ${volumeChangeColor}`}
                  >
                    {impact.before.count > 0 && impact.after.count > 0
                      ? `${impact.volume_change_pct > 0 ? '+' : ''}${impact.volume_change_pct.toFixed(1)}%`
                      : 'N/A'}
                  </td>
                  <td className="px-4 py-4 whitespace-nowrap text-center">
                    {impact.is_significant ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300">
                        유의미
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
                        일반
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
        <h4 className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-2">
          분석 기준
        </h4>
        <ul className="text-xs text-blue-800 dark:text-blue-400 space-y-1">
          <li>• 각 이벤트 전후 30일 기간의 평균값을 비교합니다</li>
          <li>• 가격 변동이 ±5% 이상이거나 거래량 변동이 ±20% 이상이면 유의미로 판단합니다</li>
          <li>
            • 녹색은 증가, 빨간색은 감소를 나타냅니다
          </li>
          <li>• 데이터가 부족한 경우 N/A로 표시됩니다</li>
        </ul>
      </div>
    </div>
  );
}
