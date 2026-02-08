'use client';

import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { PriceTrendDataItem } from '@/types/analysis';

interface CombinedPriceVolumeChartProps {
  data: PriceTrendDataItem[];
}

export default function CombinedPriceVolumeChart({
  data,
}: CombinedPriceVolumeChartProps) {
  const chartData = data.map((item) => ({
    ...item,
    평균가격: Math.round(item.avg_price / 10000),
    거래량: item.count,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        가격 + 거래량 복합 차트
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            dataKey="year_month"
            angle={-45}
            textAnchor="end"
            height={80}
            className="text-xs fill-gray-700 dark:fill-gray-300"
          />
          <YAxis
            yAxisId="left"
            orientation="left"
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '평균 가격 (억원)',
              angle: -90,
              position: 'insideLeft',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
            tickFormatter={(value: number) => value.toLocaleString('ko-KR')}
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
            tickFormatter={(value: number) => value.toLocaleString('ko-KR')}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
            }}
            formatter={(value: number, name: string) => {
              if (name === '평균가격') {
                return [`${value.toLocaleString('ko-KR')}억원`, name];
              }
              return [`${value.toLocaleString('ko-KR')}건`, name];
            }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Bar
            yAxisId="right"
            dataKey="거래량"
            fill="#10b981"
            opacity={0.6}
            name="거래량"
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="평균가격"
            stroke="#3b82f6"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="평균가격"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
