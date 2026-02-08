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
} from 'recharts';
import { PricePerAreaTrendItem } from '@/types/analysis';

interface PricePerAreaTrendChartProps {
  data: PricePerAreaTrendItem[];
}

export default function PricePerAreaTrendChart({ data }: PricePerAreaTrendChartProps) {
  const chartData = data.map((item) => ({
    월: item.year_month,
    평균평당가: Math.round(item.avg_price_per_area),
    중앙평당가: Math.round(item.median_price_per_area),
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        월별 평당가 추이
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            dataKey="월"
            className="text-xs fill-gray-700 dark:fill-gray-300"
          />
          <YAxis
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '평당가 (만원/㎡)',
              angle: -90,
              position: 'insideLeft',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
            }}
            formatter={(value: number) => `${value.toLocaleString('ko-KR')}만원/㎡`}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Line
            type="monotone"
            dataKey="평균평당가"
            stroke="#3b82f6"
            strokeWidth={3}
            dot={{ fill: '#3b82f6', r: 4 }}
            name="평균 평당가"
          />
          <Line
            type="monotone"
            dataKey="중앙평당가"
            stroke="#10b981"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#10b981', r: 3 }}
            name="중앙 평당가"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
