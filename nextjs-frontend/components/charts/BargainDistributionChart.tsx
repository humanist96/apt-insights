'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from 'recharts';
import { BargainSalesRegion } from '@/types/analysis';

interface BargainDistributionChartProps {
  data: BargainSalesRegion[];
}

export default function BargainDistributionChart({ data }: BargainDistributionChartProps) {
  const chartData = data.slice(0, 10).map((item) => ({
    ...item,
    name: item.region,
    value: item.bargain_count,
  }));

  const getColor = (rate: number) => {
    if (rate >= 0.5) return '#dc2626';
    if (rate >= 0.4) return '#ea580c';
    if (rate >= 0.3) return '#f59e0b';
    return '#10b981';
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-semibold text-gray-900 dark:text-white">{data.region}</p>
          <div className="mt-2 space-y-1 text-sm">
            <p className="text-gray-900 dark:text-white">
              급매물 수: {data.bargain_count.toLocaleString('ko-KR')}건
            </p>
            <p className="text-gray-900 dark:text-white">
              전체 거래: {data.total_count.toLocaleString('ko-KR')}건
            </p>
            <p className="text-blue-600 dark:text-blue-400 font-semibold">
              급매율: {data.bargain_rate.toFixed(2)}%
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        지역별 급매물 분포 TOP 10
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        지역별 급매물 건수와 급매율을 보여줍니다.
      </p>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 80,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={100}
            className="text-gray-600 dark:text-gray-400"
          />
          <YAxis
            label={{
              value: '급매물 수 (건)',
              angle: -90,
              position: 'insideLeft',
            }}
            className="text-gray-600 dark:text-gray-400"
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar dataKey="value" name="급매물 수" radius={[8, 8, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.bargain_rate)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-4 flex flex-wrap gap-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-red-600"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">매우 높음 (0.5% 이상)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-orange-600"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">높음 (0.4-0.5%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-amber-500"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">보통 (0.3-0.4%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded bg-emerald-500"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">낮음 (0.3% 미만)</span>
        </div>
      </div>
    </div>
  );
}
