'use client';

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { PriceTrendDataItem } from '@/types/analysis';

interface TransactionVolumeChartProps {
  data: PriceTrendDataItem[];
}

export default function TransactionVolumeChart({ data }: TransactionVolumeChartProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        거래량 추이
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <defs>
            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0.1} />
            </linearGradient>
          </defs>
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
              value: '거래 건수',
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
            formatter={(value: number) => {
              return [`${value.toLocaleString('ko-KR')}건`, '거래량'];
            }}
          />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#10b981"
            strokeWidth={2}
            fill="url(#colorCount)"
            name="거래량"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
