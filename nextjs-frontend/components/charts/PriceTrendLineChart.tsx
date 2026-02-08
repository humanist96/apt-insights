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
import { PriceTrendDataItem } from '@/types/analysis';

interface PriceTrendLineChartProps {
  data: PriceTrendDataItem[];
}

export default function PriceTrendLineChart({ data }: PriceTrendLineChartProps) {
  const chartData = data.map((item) => ({
    ...item,
    평균가격: Math.round(item.avg_price / 10000),
    중앙가격: Math.round(item.median_price / 10000),
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        평균 거래가 추이
      </h3>
      <ResponsiveContainer width="100%" height={400}>
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
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
            }}
            formatter={(value: number, name: string) => {
              return [`${value.toLocaleString('ko-KR')}억원`, name];
            }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
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
    </div>
  );
}
