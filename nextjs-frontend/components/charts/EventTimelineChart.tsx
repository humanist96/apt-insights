'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import { PriceTrendDataItem } from '@/types/analysis';
import { EventItem } from '@/types/analysis';

interface EventTimelineChartProps {
  data: PriceTrendDataItem[];
  events: EventItem[];
  onEventClick?: (event: EventItem) => void;
}

const EVENT_TYPE_COLORS: Record<string, string> = {
  정책발표: '#3b82f6',
  금리변동: '#10b981',
  재건축: '#8b5cf6',
  입주시작: '#f59e0b',
  기타: '#6b7280',
};

export default function EventTimelineChart({
  data,
  events,
  onEventClick,
}: EventTimelineChartProps) {
  const chartData = data.map((item) => ({
    ...item,
    평균가격: Math.round(item.avg_price / 10000),
    중앙가격: Math.round(item.median_price / 10000),
  }));

  const eventMarkers = events.map((event) => {
    const eventYearMonth = event.date.slice(0, 7);
    return {
      ...event,
      yearMonth: eventYearMonth,
    };
  });

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (!active || !payload || !payload.length) {
      return null;
    }

    const eventAtMonth = eventMarkers.filter((e) => e.yearMonth === label);

    return (
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3 shadow-lg">
        <p className="text-sm font-semibold text-gray-900 dark:text-white mb-2">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="text-sm text-gray-700 dark:text-gray-300">
            <span style={{ color: entry.color }}>{entry.name}: </span>
            {entry.value.toLocaleString('ko-KR')}억원
          </p>
        ))}
        {eventAtMonth.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
            {eventAtMonth.map((event) => {
              const typeConfig = EVENT_TYPE_COLORS[event.type] || EVENT_TYPE_COLORS['기타'];
              return (
                <div key={event.id} className="mb-1">
                  <p className="text-xs font-semibold" style={{ color: typeConfig }}>
                    {event.name}
                  </p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">{event.type}</p>
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        이벤트 타임라인 차트
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        가격 추이와 주요 이벤트를 함께 표시합니다. 세로선은 이벤트 발생 시점을 나타냅니다.
      </p>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            dataKey="year_month"
            angle={-45}
            textAnchor="end"
            height={80}
            className="text-xs fill-gray-700 dark:fill-gray-300"
          />
          <YAxis
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '가격 (억원)',
              angle: -90,
              position: 'insideLeft',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
            tickFormatter={(value: number) => value.toLocaleString('ko-KR')}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />

          {eventMarkers.map((event) => (
            <ReferenceLine
              key={event.id}
              x={event.yearMonth}
              stroke={EVENT_TYPE_COLORS[event.type] || EVENT_TYPE_COLORS['기타']}
              strokeWidth={2}
              strokeDasharray="5 5"
              label={{
                value: event.name,
                position: 'top',
                fill: EVENT_TYPE_COLORS[event.type] || EVENT_TYPE_COLORS['기타'],
                fontSize: 10,
                angle: -45,
              }}
              style={{ cursor: onEventClick ? 'pointer' : 'default' }}
            />
          ))}

          <Line
            type="monotone"
            dataKey="평균가격"
            stroke="#3b82f6"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="평균 가격"
          />
          <Line
            type="monotone"
            dataKey="중앙가격"
            stroke="#f59e0b"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 3 }}
            activeDot={{ r: 5 }}
            name="중앙 가격"
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-0.5 bg-blue-600"></div>
          <span className="text-gray-700 dark:text-gray-300">평균 가격</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-0.5 bg-amber-600 border-dashed border-t-2"></div>
          <span className="text-gray-700 dark:text-gray-300">중앙 가격</span>
        </div>
        {Object.entries(EVENT_TYPE_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-2">
            <div className="w-4 h-0.5 border-dashed border-t-2" style={{ borderColor: color }}></div>
            <span className="text-gray-700 dark:text-gray-300">{type}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
