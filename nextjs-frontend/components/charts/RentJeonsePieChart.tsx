'use client';

import { RentVsJeonseStats } from '@/types/analysis';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';

interface RentJeonsePieChartProps {
  stats: RentVsJeonseStats;
}

const COLORS = {
  jeonse: '#3b82f6',
  wolse: '#ef4444',
};

export default function RentJeonsePieChart({ stats }: RentJeonsePieChartProps) {
  const data = [
    { name: '전세', value: stats.jeonse_count, percentage: stats.jeonse_ratio },
    { name: '월세', value: stats.wolse_count, percentage: stats.wolse_ratio },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        전세 vs 월세 거래 비율
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percentage }) => `${name} ${percentage.toFixed(1)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.name === '전세' ? COLORS.jeonse : COLORS.wolse}
              />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: number) => `${value.toLocaleString('ko-KR')}건`}
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #ccc',
              borderRadius: '4px',
            }}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
