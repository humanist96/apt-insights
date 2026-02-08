'use client';

import { useState } from 'react';
import { useEventAnalysis } from '@/hooks/useEventAnalysis';
import EventManager from '@/components/EventManager';
import EventTimelineChart from '@/components/charts/EventTimelineChart';
import EventImpactTable from '@/components/EventImpactTable';
import RegionFilter from '@/components/filters/RegionFilter';
import StatsCard from '@/components/stats/StatsCard';

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
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          시기 이벤트 분석
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          주요 이벤트가 시장에 미친 영향을 분석합니다
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

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="등록된 이벤트"
          value={events.length.toLocaleString('ko-KR')}
          subtitle="Total Events"
        />
        <StatsCard
          title="유의미한 이벤트"
          value={significantEventsCount.toLocaleString('ko-KR')}
          subtitle="Significant Events"
        />
        <StatsCard
          title="평균 가격 변동"
          value={`${avgPriceChange > 0 ? '+' : ''}${avgPriceChange.toFixed(1)}%`}
          subtitle="Avg Price Change"
        />
        <StatsCard
          title="평균 거래량 변동"
          value={`${avgVolumeChange > 0 ? '+' : ''}${avgVolumeChange.toFixed(1)}%`}
          subtitle="Avg Volume Change"
        />
      </div>

      <div className="space-y-6">
        <EventManager
          events={events}
          onAdd={addEvent}
          onUpdate={updateEvent}
          onDelete={deleteEvent}
          onResetDefaults={resetToDefaults}
        />

        {trendData.length > 0 ? (
          <>
            <EventTimelineChart data={trendData} events={events} />
            <EventImpactTable impacts={eventImpacts} />
          </>
        ) : (
          <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-12 text-center">
            <p className="text-gray-600 dark:text-gray-400 text-lg mb-2">
              표시할 가격 추이 데이터가 없습니다
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-500">
              기간을 선택하거나 데이터를 확인해주세요
            </p>
          </div>
        )}
      </div>

      <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-300 mb-3">
          이벤트 분석 가이드
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800 dark:text-blue-400">
          <div>
            <h4 className="font-semibold mb-2">이벤트 타입</h4>
            <ul className="space-y-1">
              <li>• 정책발표: 부동산 정책, 세금 정책 변화</li>
              <li>• 금리변동: 기준금리, 대출금리 변동</li>
              <li>• 재건축: 재건축/재개발 관련 이슈</li>
              <li>• 입주시작: 대규모 단지 입주</li>
              <li>• 기타: 경제 위기, 자연재해 등</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">분석 방법</h4>
            <ul className="space-y-1">
              <li>• 이벤트 전후 30일 데이터 비교</li>
              <li>• 가격 변동 ±5% 이상: 유의미</li>
              <li>• 거래량 변동 ±20% 이상: 유의미</li>
              <li>• 타임라인 차트로 시각화</li>
              <li>• 이벤트별 영향도 분석 테이블 제공</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
