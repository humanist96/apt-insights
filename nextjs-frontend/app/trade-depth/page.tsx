'use client';

import { useState } from 'react';
import { useTradeDepth } from '@/hooks/useTradeDepth';
import RegionFilter from '@/components/filters/RegionFilter';
import StatsCard from '@/components/stats/StatsCard';
import DealingTypeChart from '@/components/charts/DealingTypeChart';
import BuyerSellerChart from '@/components/charts/BuyerSellerChart';
import MarketSignalCard from '@/components/MarketSignalCard';

export default function TradeDepthPage() {
  const [region, setRegion] = useState<string>('all');
  const [activeTab, setActiveTab] = useState<'dealing' | 'buyer-seller' | 'cancelled'>('dealing');
  const { data, isLoading, error } = useTradeDepth(region);

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            매매 심층 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            거래유형, 매수자/매도자 유형, 취소거래 분석
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
            매매 심층 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            거래유형, 매수자/매도자 유형, 취소거래 분석
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
            매매 심층 분석
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            거래유형, 매수자/매도자 유형, 취소거래 분석
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

  const { dealing_type, buyer_seller, cancelled_deals, market_signals } = data.data;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          매매 심층 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          거래유형, 매수자/매도자 유형, 취소거래 분석
        </p>
      </div>

      <div className="mb-6">
        <RegionFilter value={region} onChange={setRegion} />
      </div>

      <div className="mb-6">
        <div className="flex gap-2 border-b border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setActiveTab('dealing')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'dealing'
                ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            거래유형 분석
          </button>
          <button
            onClick={() => setActiveTab('buyer-seller')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'buyer-seller'
                ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            매수자/매도자 분석
          </button>
          <button
            onClick={() => setActiveTab('cancelled')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'cancelled'
                ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            }`}
          >
            취소거래 분석
          </button>
        </div>
      </div>

      {activeTab === 'dealing' && dealing_type.has_data && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatsCard
              title="중개거래"
              value={`${dealing_type.stats.broker_count.toLocaleString('ko-KR')}건`}
              subtitle={`${dealing_type.stats.broker_ratio.toFixed(1)}%`}
            />
            <StatsCard
              title="직거래"
              value={`${dealing_type.stats.direct_count.toLocaleString('ko-KR')}건`}
              subtitle={`${dealing_type.stats.direct_ratio.toFixed(1)}%`}
            />
            <StatsCard
              title="중개거래 평균가"
              value={`${Math.round(dealing_type.stats.broker_avg_price / 10000).toLocaleString('ko-KR')}억원`}
              subtitle="Broker Average"
            />
            <StatsCard
              title="직거래 평균가"
              value={`${Math.round(dealing_type.stats.direct_avg_price / 10000).toLocaleString('ko-KR')}억원`}
              subtitle="Direct Average"
            />
          </div>

          {dealing_type.stats.price_diff !== 0 && (
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <p className="text-blue-900 dark:text-blue-300">
                중개거래가 직거래보다 평균{' '}
                <span className="font-semibold">
                  {dealing_type.stats.price_diff > 0 ? '+' : ''}
                  {Math.round(dealing_type.stats.price_diff / 10000).toLocaleString('ko-KR')}억원
                </span>{' '}
                ({dealing_type.stats.price_diff_pct > 0 ? '+' : ''}
                {dealing_type.stats.price_diff_pct.toFixed(1)}%){' '}
                {dealing_type.stats.price_diff > 0 ? '더 비쌉니다' : '더 저렴합니다'}
              </p>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <DealingTypeChart stats={dealing_type.stats} />
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                지역별 직거래 비율 TOP 5
              </h3>
              <div className="space-y-3">
                {dealing_type.by_region.slice(0, 5).map((item) => (
                  <div key={item.region} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {item.region}
                    </span>
                    <div className="flex items-center gap-2">
                      <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${item.direct_ratio}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-semibold text-gray-900 dark:text-white w-12 text-right">
                        {item.direct_ratio.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {dealing_type.by_price_range.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                가격대별 거래 유형
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead>
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        가격대
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        중개거래
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        직거래
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        전체
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {dealing_type.by_price_range.map((row) => (
                      <tr key={row.price_range}>
                        <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                          {row.price_range}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                          {row.broker_count.toLocaleString('ko-KR')}건 ({row.broker_ratio.toFixed(1)}%)
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                          {row.direct_count.toLocaleString('ko-KR')}건 ({row.direct_ratio.toFixed(1)}%)
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                          {row.total_count.toLocaleString('ko-KR')}건
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'buyer-seller' && buyer_seller.has_data && (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              매수자 유형
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <StatsCard
                title="법인 매수"
                value={`${buyer_seller.stats.buyer_법인_count.toLocaleString('ko-KR')}건`}
                subtitle={`${buyer_seller.stats.buyer_법인_ratio.toFixed(1)}%`}
              />
              <StatsCard
                title="개인 매수"
                value={`${buyer_seller.stats.buyer_개인_count.toLocaleString('ko-KR')}건`}
                subtitle={`${buyer_seller.stats.buyer_개인_ratio.toFixed(1)}%`}
              />
              <StatsCard
                title="미공개"
                value={`${buyer_seller.stats.buyer_미공개_count.toLocaleString('ko-KR')}건`}
                subtitle={`${buyer_seller.stats.buyer_미공개_ratio.toFixed(1)}%`}
              />
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              매도자 유형
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <StatsCard
                title="법인 매도"
                value={`${buyer_seller.stats.seller_법인_count.toLocaleString('ko-KR')}건`}
                subtitle={`${buyer_seller.stats.seller_법인_ratio.toFixed(1)}%`}
              />
              <StatsCard
                title="개인 매도"
                value={`${buyer_seller.stats.seller_개인_count.toLocaleString('ko-KR')}건`}
                subtitle={`${buyer_seller.stats.seller_개인_ratio.toFixed(1)}%`}
              />
              <StatsCard
                title="미공개"
                value={`${buyer_seller.stats.seller_미공개_count.toLocaleString('ko-KR')}건`}
                subtitle={`${buyer_seller.stats.seller_미공개_ratio.toFixed(1)}%`}
              />
            </div>
          </div>

          {buyer_seller.stats.buyer_법인_count > buyer_seller.stats.seller_법인_count ? (
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <p className="text-green-900 dark:text-green-300">
                법인 순매수: 법인 매수({buyer_seller.stats.buyer_법인_count}건) &gt; 법인 매도(
                {buyer_seller.stats.seller_법인_count}건) → 투자 유입 신호
              </p>
            </div>
          ) : buyer_seller.stats.buyer_법인_count < buyer_seller.stats.seller_법인_count ? (
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
              <p className="text-yellow-900 dark:text-yellow-300">
                법인 순매도: 법인 매수({buyer_seller.stats.buyer_법인_count}건) &lt; 법인 매도(
                {buyer_seller.stats.seller_법인_count}건) → 투자 이탈 신호
              </p>
            </div>
          ) : null}

          <BuyerSellerChart data={buyer_seller.by_region} />
        </div>
      )}

      {activeTab === 'cancelled' && cancelled_deals.has_data && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatsCard
              title="전체 거래"
              value={`${cancelled_deals.stats.total_count.toLocaleString('ko-KR')}건`}
              subtitle="Total Transactions"
            />
            <StatsCard
              title={`${cancelled_deals.stats.cancel_ratio >= 10 ? '🔴' : cancelled_deals.stats.cancel_ratio >= 5 ? '🟡' : '🟢'} 취소 거래`}
              value={`${cancelled_deals.stats.cancelled_count.toLocaleString('ko-KR')}건`}
              subtitle={`${cancelled_deals.stats.cancel_ratio.toFixed(1)}%`}
            />
            <StatsCard
              title="취소거래 평균가"
              value={`${Math.round(cancelled_deals.stats.cancelled_avg_price / 10000).toLocaleString('ko-KR')}억원`}
              subtitle="Cancelled Average"
            />
            <StatsCard
              title="정상거래 평균가"
              value={`${Math.round(cancelled_deals.stats.normal_avg_price / 10000).toLocaleString('ko-KR')}억원`}
              subtitle="Normal Average"
            />
          </div>

          {Object.keys(cancelled_deals.stats.cancel_types).length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                취소 유형별 현황
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {Object.entries(cancelled_deals.stats.cancel_types).map(([type, count]) => (
                  <div
                    key={type}
                    className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4"
                  >
                    <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      {type}
                    </div>
                    <div className="text-2xl font-bold text-gray-900 dark:text-white">
                      {count.toLocaleString('ko-KR')}건
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {cancelled_deals.cancelled_items.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                취소거래 상세 목록
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead>
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        아파트
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        지역
                      </th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        가격(만원)
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        취소유형
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        거래일
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {cancelled_deals.cancelled_items.map((item, index) => (
                      <tr key={index}>
                        <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                          {item.apt_name}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                          {item.region}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-right text-gray-700 dark:text-gray-300">
                          {item.price.toLocaleString('ko-KR')}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                          {item.cancel_type}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                          {item.deal_date}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {market_signals.length > 0 && (
        <div className="mt-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            종합 시장 신호
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {market_signals.map((signal, index) => (
              <MarketSignalCard key={index} signal={signal} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
