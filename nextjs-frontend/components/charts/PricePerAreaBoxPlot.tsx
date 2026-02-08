'use client';

import {
  ComposedChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { PricePerAreaByRegion } from '@/types/analysis';

interface PricePerAreaBoxPlotProps {
  data: PricePerAreaByRegion[];
}

export default function PricePerAreaBoxPlot({ data }: PricePerAreaBoxPlotProps) {
  const chartData = data.map((item) => ({
    region: item.region,
    min: Math.round(item.min_price_per_area),
    median: Math.round(item.median_price_per_area),
    max: Math.round(item.max_price_per_area),
    avg: Math.round(item.avg_price_per_area),
  }));

  const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        지역별 평당가 분포
      </h3>
      <div className="mb-4 text-sm text-gray-600 dark:text-gray-400">
        <p>각 지역의 최저가, 중앙값, 평균, 최고가를 나타냅니다.</p>
      </div>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            dataKey="region"
            angle={-45}
            textAnchor="end"
            height={100}
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
          <Bar dataKey="max" stackId="a" fill="transparent" />
          <Bar dataKey="avg" stackId="a">
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
          <Bar dataKey="min" stackId="a" fill="transparent" />
        </ComposedChart>
      </ResponsiveContainer>
      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-500 rounded"></div>
          <span className="text-gray-700 dark:text-gray-300">평균</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded"></div>
          <span className="text-gray-700 dark:text-gray-300">중앙값</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-red-500 rounded"></div>
          <span className="text-gray-700 dark:text-gray-300">최고가</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-gray-400 rounded"></div>
          <span className="text-gray-700 dark:text-gray-300">최저가</span>
        </div>
      </div>
    </div>
  );
}
