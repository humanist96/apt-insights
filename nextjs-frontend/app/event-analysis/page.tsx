'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Star, TrendingUp, BarChart3, Info } from 'lucide-react';
import { useEventAnalysis } from '@/hooks/useEventAnalysis';
import EventManager from '@/components/EventManager';
import EventTimelineChart from '@/components/charts/EventTimelineChart';
import EventImpactTable from '@/components/EventImpactTable';
import RegionFilter from '@/components/filters/RegionFilter';

export default function EventAnalysisPage() {
  const [region, setRegion] = useState<string>('all');
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');

  const {
    events,
    eventImpacts,
    addEvent,
    updateEvent,
    deleteEvent,
    resetToDefaults,
    trendData,
  } = useEventAnalysis(startDate, endDate, region !== 'all' ? region : undefined);

  const significantEventsCount = eventImpacts.filter((impact) => impact.is_significant).length;
  const avgPriceChange =
    eventImpacts.length > 0
      ? eventImpacts.reduce((sum, impact) => sum + impact.price_change_pct, 0) /
        eventImpacts.length
      : 0;
  const avgVolumeChange =
    eventImpacts.length > 0
      ? eventImpacts.reduce((sum, impact) => sum + impact.volume_change_pct, 0) /
        eventImpacts.length
      : 0;

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Animated background orbs */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -left-32 top-0 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500/20 to-blue-500/20 blur-3xl"
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
          className="absolute -right-32 top-1/3 h-96 w-96 rounded-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 blur-3xl"
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
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-purple-500/20 bg-purple-500/10 px-4 py-2 backdrop-blur-sm">
            <Calendar className="h-4 w-4 text-purple-400" />
            <span className="text-sm font-medium text-purple-300">시기 이벤트</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-purple-200 via-blue-200 to-indigo-200 bg-clip-text text-5xl font-bold text-transparent">
            시기 이벤트 분석
          </h1>
          <p className="text-lg text-slate-400">
            주요 이벤트가 시장에 미친 영향을 분석합니다
          </p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3"
        >
          <div>
            <label
              htmlFor="region-filter"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-purple-400" />
                지역 선택
              </div>
            </label>
            <RegionFilter value={region} onChange={setRegion} />
          </div>

          <div>
            <label
              htmlFor="start-date"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-blue-400" />
                시작일
              </div>
            </label>
            <input
              type="month"
              id="start-date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-3 text-slate-200 backdrop-blur-sm transition-all placeholder:text-slate-500 hover:border-blue-500/50 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
            />
          </div>

          <div>
            <label
              htmlFor="end-date"
              className="mb-2 block text-sm font-medium text-slate-300"
            >
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-indigo-400" />
                종료일
              </div>
            </label>
            <input
              type="month"
              id="end-date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-3 text-slate-200 backdrop-blur-sm transition-all placeholder:text-slate-500 hover:border-indigo-500/50 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            />
          </div>
        </motion.div>

        {/* Stats Cards */}
        <div className="mb-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {[
            {
              title: '등록된 이벤트',
              value: events.length.toLocaleString('ko-KR'),
              subtitle: 'Total Events',
              gradient: 'from-purple-500 to-indigo-500',
              icon: Calendar,
            },
            {
              title: '유의미한 이벤트',
              value: significantEventsCount.toLocaleString('ko-KR'),
              subtitle: 'Significant Events',
              gradient: 'from-blue-500 to-cyan-500',
              icon: Star,
            },
            {
              title: '평균 가격 변동',
              value: `${avgPriceChange > 0 ? '+' : ''}${avgPriceChange.toFixed(1)}%`,
              subtitle: 'Avg Price Change',
              gradient: 'from-green-500 to-emerald-500',
              icon: TrendingUp,
            },
            {
              title: '평균 거래량 변동',
              value: `${avgVolumeChange > 0 ? '+' : ''}${avgVolumeChange.toFixed(1)}%`,
              subtitle: 'Avg Volume Change',
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
                transition={{ duration: 0.6, delay: 0.2 + index * 0.1 }}
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
                  <p className="mb-1 text-3xl font-bold text-slate-100">
                    {stat.value}
                  </p>
                  <p className="text-xs text-slate-500">{stat.subtitle}</p>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Event Manager */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mb-8 overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm"
        >
          <EventManager
            events={events}
            onAdd={addEvent}
            onUpdate={updateEvent}
            onDelete={deleteEvent}
            onResetDefaults={resetToDefaults}
          />
        </motion.div>

        {/* Charts and Tables */}
        {trendData.length > 0 ? (
          <div className="space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.7 }}
              className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 p-8 backdrop-blur-sm"
            >
              <EventTimelineChart data={trendData} events={events} />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-sm"
            >
              <EventImpactTable impacts={eventImpacts} />
            </motion.div>
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
            className="rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/30 to-slate-900/30 p-16 text-center backdrop-blur-sm"
          >
            <div className="mx-auto mb-4 inline-flex rounded-full bg-slate-800/50 p-4">
              <Info className="h-8 w-8 text-slate-500" />
            </div>
            <p className="mb-2 text-xl font-medium text-slate-400">
              표시할 가격 추이 데이터가 없습니다
            </p>
            <p className="text-sm text-slate-500">
              기간을 선택하거나 데이터를 확인해주세요
            </p>
          </motion.div>
        )}

        {/* Guide Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.9 }}
          className="mt-12 overflow-hidden rounded-3xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/5 p-8 backdrop-blur-sm"
        >
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-gradient-to-br from-blue-500 to-indigo-500 p-3">
              <Info className="h-6 w-6 text-white" />
            </div>
            <h3 className="text-2xl font-semibold text-blue-300">
              이벤트 분석 가이드
            </h3>
          </div>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            <div className="rounded-2xl border border-blue-500/10 bg-blue-500/5 p-6">
              <h4 className="mb-4 text-lg font-semibold text-blue-300">
                이벤트 타입
              </h4>
              <ul className="space-y-3 text-sm text-blue-400/80">
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                  <span>정책발표: 부동산 정책, 세금 정책 변화</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                  <span>금리변동: 기준금리, 대출금리 변동</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                  <span>재건축: 재건축/재개발 관련 이슈</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                  <span>입주시작: 대규모 단지 입주</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-blue-400" />
                  <span>기타: 경제 위기, 자연재해 등</span>
                </li>
              </ul>
            </div>
            <div className="rounded-2xl border border-indigo-500/10 bg-indigo-500/5 p-6">
              <h4 className="mb-4 text-lg font-semibold text-indigo-300">
                분석 방법
              </h4>
              <ul className="space-y-3 text-sm text-indigo-400/80">
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-indigo-400" />
                  <span>이벤트 전후 30일 데이터 비교</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-indigo-400" />
                  <span>가격 변동 ±5% 이상: 유의미</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-indigo-400" />
                  <span>거래량 변동 ±20% 이상: 유의미</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-indigo-400" />
                  <span>타임라인 차트로 시각화</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-indigo-400" />
                  <span>이벤트별 영향도 분석 테이블 제공</span>
                </li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
