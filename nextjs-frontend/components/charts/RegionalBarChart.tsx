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
import { RegionalDataItem } from '@/types/analysis';

interface RegionalBarChartProps {
  data: RegionalDataItem[];
}

export default function RegionalBarChart({ data }: RegionalBarChartProps) {
  const chartData = data.map((item) => ({
    ...item,
    평균가격: Math.round(item.avg_price / 10000), // Convert to 억원
    거래건수: item.count,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        지역별 평균 가격 및 거래 건수
      </h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            dataKey="region"
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
              if (name === '평균가격') {
                return [`${value.toLocaleString('ko-KR')}억원`, name];
              }
              return [`${value.toLocaleString('ko-KR')}건`, name];
            }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Bar yAxisId="left" dataKey="평균가격" fill="#3b82f6" name="평균 가격" />
          <Bar yAxisId="right" dataKey="거래건수" fill="#10b981" name="거래 건수" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
