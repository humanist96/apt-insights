import { useState, useEffect, useMemo } from 'react';
import { EventItem, EventImpact } from '@/types/analysis';
import { usePriceTrend } from './usePriceTrend';

const STORAGE_KEY = 'apt-event-analysis-events';
const ANALYSIS_WINDOW_DAYS = 30;

export function useEventAnalysis(startDate?: string, endDate?: string, region?: string) {
  const [events, setEvents] = useState<EventItem[]>([]);

  const { data: trendData } = usePriceTrend({
    startDate,
    endDate,
    regionFilter: region,
  });

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setEvents(parsed);
      } catch {
        setEvents(getDefaultEvents());
      }
    } else {
      const defaultEvents = getDefaultEvents();
      setEvents(defaultEvents);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultEvents));
    }
  }, []);

  const addEvent = (event: Omit<EventItem, 'id'>) => {
    const newEvent: EventItem = {
      ...event,
      id: `event-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    };

    const updatedEvents = [...events, newEvent];
    setEvents(updatedEvents);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedEvents));

    return newEvent;
  };

  const updateEvent = (id: string, updates: Partial<EventItem>) => {
    const updatedEvents = events.map((event) =>
      event.id === id ? { ...event, ...updates } : event
    );
    setEvents(updatedEvents);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedEvents));
  };

  const deleteEvent = (id: string) => {
    const updatedEvents = events.filter((event) => event.id !== id);
    setEvents(updatedEvents);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedEvents));
  };

  const resetToDefaults = () => {
    const defaultEvents = getDefaultEvents();
    setEvents(defaultEvents);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultEvents));
  };

  const eventImpacts = useMemo<EventImpact[]>(() => {
    if (!trendData?.data?.trend_data || events.length === 0) {
      return [];
    }

    const trendItems = trendData.data.trend_data;

    return events.map((event) => {
      const eventDate = new Date(event.date);
      const beforeStart = new Date(eventDate);
      beforeStart.setDate(beforeStart.getDate() - ANALYSIS_WINDOW_DAYS);
      const afterEnd = new Date(eventDate);
      afterEnd.setDate(afterEnd.getDate() + ANALYSIS_WINDOW_DAYS);

      const beforeItems = trendItems.filter((item) => {
        const itemDate = new Date(item.year_month + '-01');
        return itemDate >= beforeStart && itemDate < eventDate;
      });

      const afterItems = trendItems.filter((item) => {
        const itemDate = new Date(item.year_month + '-01');
        return itemDate > eventDate && itemDate <= afterEnd;
      });

      const beforeAvgPrice =
        beforeItems.length > 0
          ? beforeItems.reduce((sum, item) => sum + item.avg_price, 0) / beforeItems.length
          : 0;
      const beforeCount = beforeItems.reduce((sum, item) => sum + item.count, 0);

      const afterAvgPrice =
        afterItems.length > 0
          ? afterItems.reduce((sum, item) => sum + item.avg_price, 0) / afterItems.length
          : 0;
      const afterCount = afterItems.reduce((sum, item) => sum + item.count, 0);

      const priceChangePct =
        beforeAvgPrice > 0 ? ((afterAvgPrice - beforeAvgPrice) / beforeAvgPrice) * 100 : 0;
      const volumeChangePct =
        beforeCount > 0 ? ((afterCount - beforeCount) / beforeCount) * 100 : 0;

      const isSignificant = Math.abs(priceChangePct) > 5 || Math.abs(volumeChangePct) > 20;

      return {
        event,
        before: {
          avg_price: beforeAvgPrice,
          count: beforeCount,
          period_days: ANALYSIS_WINDOW_DAYS,
        },
        after: {
          avg_price: afterAvgPrice,
          count: afterCount,
          period_days: ANALYSIS_WINDOW_DAYS,
        },
        price_change_pct: priceChangePct,
        volume_change_pct: volumeChangePct,
        is_significant: isSignificant,
      };
    });
  }, [events, trendData]);

  return {
    events,
    eventImpacts,
    addEvent,
    updateEvent,
    deleteEvent,
    resetToDefaults,
    trendData: trendData?.data?.trend_data || [],
  };
}

function getDefaultEvents(): EventItem[] {
  return [
    {
      id: 'default-1',
      name: '기준금리 인상',
      date: '2023-01-15',
      description: '한국은행 기준금리 3.5%로 인상',
      type: '금리변동',
    },
    {
      id: 'default-2',
      name: '대출규제 강화',
      date: '2023-03-20',
      description: 'DSR 규제 강화 정책 발표',
      type: '정책발표',
    },
    {
      id: 'default-3',
      name: '재건축 규제 완화',
      date: '2023-05-10',
      description: '재건축 초과이익환수제 완화',
      type: '재건축',
    },
    {
      id: 'default-4',
      name: '신규 단지 입주',
      date: '2023-07-01',
      description: '대규모 신축 아파트 단지 입주 시작',
      type: '입주시작',
    },
    {
      id: 'default-5',
      name: '경기 침체 우려',
      date: '2023-09-15',
      description: '글로벌 경기 침체 우려 확대',
      type: '기타',
    },
  ];
}
