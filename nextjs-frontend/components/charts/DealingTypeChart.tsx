'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { DealingTypeStats } from '@/types/analysis';

interface DealingTypeChartProps {
  stats: DealingTypeStats;
}

const COLORS = ['#3b82f6', '#ef4444'];

export default function DealingTypeChart({ stats }: DealingTypeChartProps) {
  const data = [
    { name: '중개거래', value: stats.broker_count, ratio: stats.broker_ratio },
    { name: '직거래', value: stats.direct_count, ratio: stats.direct_ratio },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        거래 유형 비율
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, ratio }) => `${name} ${ratio.toFixed(1)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
            }}
            formatter={(value: number) => [`${value.toLocaleString('ko-KR')}건`, '거래 수']}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
