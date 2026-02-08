'use client';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { AreaAnalysisDataItem } from '@/types/analysis';

interface AreaPricePerAreaChartProps {
  data: AreaAnalysisDataItem[];
}

export default function AreaPricePerAreaChart({ data }: AreaPricePerAreaChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          면적대별 ㎡당 가격 비교
        </h3>
        <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
          데이터가 없습니다
        </div>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    name: item.area_range.replace('~', '-') + '㎡',
    value: Math.round(item.price_per_area),
    fullData: item,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        면적대별 ㎡당 가격 비교
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
          <XAxis
            dataKey="name"
            stroke="#6b7280"
            angle={-45}
            textAnchor="end"
            height={100}
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <YAxis
            stroke="#6b7280"
            tick={{ fill: '#6b7280' }}
            label={{ value: '㎡당 가격 (만원)', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '0.5rem',
              color: '#f3f4f6',
            }}
            formatter={(value: number) => [value.toLocaleString('ko-KR') + '만원/㎡', '㎡당 가격']}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#8b5cf6"
            strokeWidth={3}
            dot={{ fill: '#8b5cf6', r: 6 }}
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
