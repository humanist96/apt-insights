'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { AreaAnalysisDataItem } from '@/types/analysis';

interface AreaPriceChartProps {
  data: AreaAnalysisDataItem[];
}

export default function AreaPriceChart({ data }: AreaPriceChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          면적대별 가격 비교
        </h3>
        <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
          데이터가 없습니다
        </div>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    name: item.area_range.replace('~', '-') + '㎡',
    평균가격: Math.round(item.avg_price / 10000),
    최고가격: item.max_price ? Math.round(item.max_price / 10000) : 0,
    최저가격: item.min_price ? Math.round(item.min_price / 10000) : 0,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        면적대별 가격 비교
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
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
            label={{ value: '가격 (억원)', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '0.5rem',
              color: '#f3f4f6',
            }}
            formatter={(value: number) => [value.toLocaleString('ko-KR') + '억원', '']}
          />
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          <Bar dataKey="평균가격" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          <Bar dataKey="최고가격" fill="#10b981" radius={[4, 4, 0, 0]} />
          <Bar dataKey="최저가격" fill="#f59e0b" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
