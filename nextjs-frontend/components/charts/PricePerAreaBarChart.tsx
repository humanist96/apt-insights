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
import { PricePerAreaByAreaRange } from '@/types/analysis';

interface PricePerAreaBarChartProps {
  data: PricePerAreaByAreaRange[];
}

export default function PricePerAreaBarChart({ data }: PricePerAreaBarChartProps) {
  const chartData = data.map((item) => ({
    면적대: item.area_range,
    평당가: Math.round(item.avg_price_per_area),
    거래건수: item.count,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        면적대별 평당가 분석
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            dataKey="면적대"
            angle={-45}
            textAnchor="end"
            height={100}
            className="text-xs fill-gray-700 dark:fill-gray-300"
          />
          <YAxis
            yAxisId="left"
            orientation="left"
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '평당가 (만원/㎡)',
              angle: -90,
              position: 'insideLeft',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <YAxis
            yAxisId="right"
            orientation="right"
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '거래 건수',
              angle: 90,
              position: 'insideRight',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
            }}
            formatter={(value: number, name: string) => {
              if (name === '평당가') {
                return [`${value.toLocaleString('ko-KR')}만원/㎡`, name];
              }
              return [`${value.toLocaleString('ko-KR')}건`, name];
            }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Bar yAxisId="left" dataKey="평당가" fill="#3b82f6" name="평당가" />
          <Bar yAxisId="right" dataKey="거래건수" fill="#10b981" name="거래 건수" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
