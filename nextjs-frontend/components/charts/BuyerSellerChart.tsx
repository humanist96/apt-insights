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
import { BuyerSellerRegion } from '@/types/analysis';

interface BuyerSellerChartProps {
  data: BuyerSellerRegion[];
}

export default function BuyerSellerChart({ data }: BuyerSellerChartProps) {
  const chartData = data.slice(0, 10).map((item) => ({
    region: item.region,
    매수법인: item.buyer_법인_ratio,
    매도법인: item.seller_법인_ratio,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        지역별 법인 거래 비율
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
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '비율 (%)',
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
            formatter={(value: number) => `${value.toFixed(1)}%`}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Bar dataKey="매수법인" fill="#3b82f6" name="법인 매수 비율" />
          <Bar dataKey="매도법인" fill="#ef4444" name="법인 매도 비율" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
