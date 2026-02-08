'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  TrendingUp,
  Users,
  Building2,
  User,
  XCircle,
  AlertTriangle,
  CheckCircle,
  Info,
  BarChart3,
} from 'lucide-react';
import { useTradeDepth } from '@/hooks/useTradeDepth';
import DealingTypeChart from '@/components/charts/DealingTypeChart';
import BuyerSellerChart from '@/components/charts/BuyerSellerChart';
import MarketSignalCard from '@/components/MarketSignalCard';
import RegionFilter from '@/components/filters/RegionFilter';
import StatsCard from '@/components/stats/StatsCard';

type TabType = 'dealing' | 'buyer-seller' | 'cancelled';

export default function TradeDepthPage() {
  const [region, setRegion] = useState<string>('all');
  const [activeTab, setActiveTab] = useState<TabType>('dealing');
  const { data, isLoading, error } = useTradeDepth(region);

  const tabs = [
    { id: 'dealing' as TabType, label: '거래유형', icon: TrendingUp },
    { id: 'buyer-seller' as TabType, label: '매수자/매도자', icon: Users },
    { id: 'cancelled' as TabType, label: '취소거래', icon: XCircle },
  ];

  if (isLoading) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="relative z-10 container mx-auto px-4 py-12">
          <div className="mb-12">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2 backdrop-blur-sm">
              <BarChart3 className="h-4 w-4 text-blue-400" />
              <span className="text-sm font-medium text-blue-300">심층 분석</span>
            </div>
            <h1 className="mb-4 bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
              매매 심층 분석
            </h1>
          </div>
          <div className="animate-pulse space-y-6">
            <div className="h-10 w-64 rounded-xl bg-slate-700/50"></div>
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-32 rounded-2xl bg-slate-700/50"></div>
              ))}
            </div>
            <div className="h-96 rounded-3xl bg-slate-700/50"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="relative z-10 container mx-auto px-4 py-12">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
              매매 심층 분석
            </h1>
          </div>
          <div className="rounded-3xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 p-8 backdrop-blur-sm">
            <div className="mb-4 flex items-center gap-3">
              <AlertTriangle className="h-6 w-6 text-red-400" />
              <h3 className="text-xl font-semibold text-red-300">
                데이터를 불러오는 중 오류가 발생했습니다
              </h3>
            </div>
            <p className="text-red-400">
              {error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!data?.success || !data?.data) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="relative z-10 container mx-auto px-4 py-12">
          <div className="mb-12">
            <h1 className="mb-4 bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
              매매 심층 분석
            </h1>
          </div>
          <div className="rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/30 to-slate-900/30 p-16 text-center backdrop-blur-sm">
            <div className="mx-auto mb-4 inline-flex rounded-full bg-slate-800/50 p-4">
              <Info className="h-8 w-8 text-slate-500" />
            </div>
            <p className="text-xl font-medium text-slate-400">표시할 데이터가 없습니다</p>
          </div>
        </div>
      </div>
    );
  }

  const { dealing_type, buyer_seller, cancelled_deals, market_signals } = data.data;

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Animated background orbs */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -left-32 top-0 h-96 w-96 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, 50, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="absolute -right-32 top-1/3 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500/20 to-pink-500/20 blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, -50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12"
        >
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2 backdrop-blur-sm">
            <BarChart3 className="h-4 w-4 text-blue-400" />
            <span className="text-sm font-medium text-blue-300">심층 분석</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
            매매 심층 분석
          </h1>
          <p className="text-lg text-slate-400">
            거래유형, 매수자/매도자 유형, 취소거래 분석
          </p>
        </motion.div>

        {/* Region Filter */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8"
        >
          <RegionFilter value={region} onChange={setRegion} />
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-8"
        >
          <div className="flex gap-2 overflow-x-auto rounded-2xl border border-slate-700/50 bg-slate-800/30 p-2 backdrop-blur-sm">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative flex items-center gap-2 rounded-xl px-6 py-3 text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-slate-700 to-slate-800 text-white shadow-lg'
                      : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-300'
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 rounded-xl bg-gradient-to-r from-slate-700 to-slate-800"
                      transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  <Icon className="relative h-4 w-4" />
                  <span className="relative whitespace-nowrap">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </motion.div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'dealing' && dealing_type.has_data && (
            <motion.div
              key="dealing"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-8"
            >
              {/* Stats Cards */}
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {[
                  {
                    title: '중개거래',
                    value: `${dealing_type.stats.broker_count.toLocaleString('ko-KR')}건`,
                    subtitle: `${dealing_type.stats.broker_ratio.toFixed(1)}%`,
                    gradient: 'from-blue-500 to-cyan-500',
                    icon: Building2,
                  },
                  {
                    title: '직거래',
                    value: `${dealing_type.stats.direct_count.toLocaleString('ko-KR')}건`,
                    subtitle: `${dealing_type.stats.direct_ratio.toFixed(1)}%`,
                    gradient: 'from-green-500 to-emerald-500',
                    icon: User,
                  },
                  {
                    title: '중개거래 평균가',
                    value: `${Math.round(dealing_type.stats.broker_avg_price / 10000).toLocaleString('ko-KR')}억원`,
                    subtitle: 'Broker Average',
                    gradient: 'from-purple-500 to-indigo-500',
                    icon: TrendingUp,
                  },
                  {
                    title: '직거래 평균가',
                    value: `${Math.round(dealing_type.stats.direct_avg_price / 10000).toLocaleString('ko-KR')}억원`,
                    subtitle: 'Direct Average',
                    gradient: 'from-amber-500 to-orange-500',
                    icon: BarChart3,
                  },
                ].map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: index * 0.1 }}
                      className="group relative overflow-hidden rounded-2xl border border-slate-700/50 bg-gradient-to-br from-slate-800/80 to-slate-900/80 p-6 backdrop-blur-sm transition-all hover:border-slate-600/50 hover:shadow-xl hover:shadow-slate-900/50"
                    >
                      <div
                        className={`absolute right-0 top-0 h-32 w-32 bg-gradient-to-br ${stat.gradient} opacity-10 blur-3xl transition-opacity group-hover:opacity-20`}
                      />
                      <div className="relative">
                        <div
                          className={`mb-4 inline-flex rounded-xl bg-gradient-to-br ${stat.gradient} p-3 shadow-lg`}
                        >
                          <Icon className="h-6 w-6 text-white" />
                        </div>
                        <h3 className="mb-2 text-sm font-medium text-slate-400">
                          {stat.title}
                        </h3>
                        <p className="mb-1 text-2xl font-bold text-slate-100">{stat.value}</p>
                        <p className="text-xs text-slate-500">{stat.subtitle}</p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>

              {/* Price difference info */}
              {dealing_type.stats.price_diff !== 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.4 }}
                  className="rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/5 p-6 backdrop-blur-sm"
                >
                  <div className="flex items-center gap-3">
                    <Info className="h-5 w-5 text-blue-400" />
                    <p className="text-blue-400">
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
                </motion.div>
              )}

              {/* Charts and tables */}
              <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.5 }}
                  className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 backdrop-blur-sm"
                >
                  <DealingTypeChart stats={dealing_type.stats} />
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.6 }}
                  className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-6 backdrop-blur-sm"
                >
                  <h3 className="mb-6 text-lg font-semibold text-slate-200">
                    지역별 직거래 비율 TOP 5
                  </h3>
                  <div className="space-y-4">
                    {dealing_type.by_region.slice(0, 5).map((item, idx) => (
                      <div key={item.region} className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-300">
                          {item.region}
                        </span>
                        <div className="flex items-center gap-3">
                          <div className="h-2 w-32 overflow-hidden rounded-full bg-slate-700">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${item.direct_ratio}%` }}
                              transition={{ duration: 0.8, delay: 0.7 + idx * 0.1 }}
                              className="h-full rounded-full bg-gradient-to-r from-blue-500 to-cyan-500"
                            />
                          </div>
                          <span className="w-12 text-right text-sm font-semibold text-slate-100">
                            {item.direct_ratio.toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              </div>

              {/* Price range table */}
              {dealing_type.by_price_range.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.7 }}
                  className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm"
                >
                  <div className="border-b border-slate-700/50 p-6">
                    <h3 className="text-lg font-semibold text-slate-200">
                      가격대별 거래 유형
                    </h3>
                  </div>
                  <div className="overflow-x-auto p-6">
                    <table className="min-w-full">
                      <thead>
                        <tr className="border-b border-slate-700/50">
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                            가격대
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                            중개거래
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                            직거래
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                            전체
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-700/30">
                        {dealing_type.by_price_range.map((row, idx) => (
                          <motion.tr
                            key={row.price_range}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: idx * 0.05 }}
                            className="transition-colors hover:bg-white/5"
                          >
                            <td className="whitespace-nowrap px-4 py-3 text-sm font-medium text-slate-200">
                              {row.price_range}
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-right text-sm text-slate-300">
                              {row.broker_count.toLocaleString('ko-KR')}건 ({row.broker_ratio.toFixed(1)}%)
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-right text-sm text-slate-300">
                              {row.direct_count.toLocaleString('ko-KR')}건 ({row.direct_ratio.toFixed(1)}%)
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-right text-sm text-slate-300">
                              {row.total_count.toLocaleString('ko-KR')}건
                            </td>
                          </motion.tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}

          {activeTab === 'buyer-seller' && buyer_seller.has_data && (
            <motion.div
              key="buyer-seller"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-8"
            >
              {/* Buyer Stats */}
              <div>
                <h3 className="mb-6 text-xl font-semibold text-slate-200">매수자 유형</h3>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
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

              {/* Seller Stats */}
              <div>
                <h3 className="mb-6 text-xl font-semibold text-slate-200">매도자 유형</h3>
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
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

              {/* Market signal */}
              {buyer_seller.stats.buyer_법인_count > buyer_seller.stats.seller_법인_count ? (
                <div className="rounded-2xl border border-green-500/20 bg-gradient-to-br from-green-500/10 to-emerald-500/5 p-6 backdrop-blur-sm">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-400" />
                    <p className="text-green-400">
                      법인 순매수: 법인 매수({buyer_seller.stats.buyer_법인_count}건) &gt; 법인 매도(
                      {buyer_seller.stats.seller_법인_count}건) → 투자 유입 신호
                    </p>
                  </div>
                </div>
              ) : buyer_seller.stats.buyer_법인_count < buyer_seller.stats.seller_법인_count ? (
                <div className="rounded-2xl border border-yellow-500/20 bg-gradient-to-br from-yellow-500/10 to-amber-500/5 p-6 backdrop-blur-sm">
                  <div className="flex items-center gap-3">
                    <AlertTriangle className="h-5 w-5 text-yellow-400" />
                    <p className="text-yellow-400">
                      법인 순매도: 법인 매수({buyer_seller.stats.buyer_법인_count}건) &lt; 법인 매도(
                      {buyer_seller.stats.seller_법인_count}건) → 투자 이탈 신호
                    </p>
                  </div>
                </div>
              ) : null}

              {/* Chart */}
              <div className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-8 backdrop-blur-sm">
                <BuyerSellerChart data={buyer_seller.by_region} />
              </div>
            </motion.div>
          )}

          {activeTab === 'cancelled' && cancelled_deals.has_data && (
            <motion.div
              key="cancelled"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="space-y-8"
            >
              {/* Stats Cards */}
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
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

              {/* Cancel types */}
              {Object.keys(cancelled_deals.stats.cancel_types).length > 0 && (
                <div className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm">
                  <div className="border-b border-slate-700/50 p-6">
                    <h3 className="text-lg font-semibold text-slate-200">
                      취소 유형별 현황
                    </h3>
                  </div>
                  <div className="grid grid-cols-1 gap-4 p-6 sm:grid-cols-3">
                    {Object.entries(cancelled_deals.stats.cancel_types).map(([type, count]) => (
                      <div
                        key={type}
                        className="rounded-xl bg-slate-900/50 p-4"
                      >
                        <div className="mb-2 text-sm text-slate-400">{type}</div>
                        <div className="text-2xl font-bold text-slate-100">
                          {(count as number).toLocaleString('ko-KR')}건
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Cancelled items table */}
              {cancelled_deals.cancelled_items.length > 0 && (
                <div className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm">
                  <div className="border-b border-slate-700/50 p-6">
                    <h3 className="text-lg font-semibold text-slate-200">
                      취소거래 상세 목록
                    </h3>
                  </div>
                  <div className="overflow-x-auto p-6">
                    <table className="min-w-full">
                      <thead>
                        <tr className="border-b border-slate-700/50">
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                            아파트
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                            지역
                          </th>
                          <th className="px-4 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-400">
                            가격(만원)
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                            취소유형
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-400">
                            거래일
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-700/30">
                        {cancelled_deals.cancelled_items.map((item: any, index: number) => (
                          <motion.tr
                            key={index}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: index * 0.05 }}
                            className="transition-colors hover:bg-white/5"
                          >
                            <td className="whitespace-nowrap px-4 py-3 text-sm font-medium text-slate-200">
                              {item.apt_name}
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-sm text-slate-300">
                              {item.region}
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-right text-sm text-slate-300">
                              {item.price.toLocaleString('ko-KR')}
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-sm text-slate-300">
                              {item.cancel_type}
                            </td>
                            <td className="whitespace-nowrap px-4 py-3 text-sm text-slate-300">
                              {item.deal_date}
                            </td>
                          </motion.tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Market signals */}
        {market_signals.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1 }}
            className="mt-12"
          >
            <h2 className="mb-6 text-2xl font-semibold text-slate-200">종합 시장 신호</h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              {market_signals.map((signal: any, index: number) => (
                <MarketSignalCard key={index} signal={signal} />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
