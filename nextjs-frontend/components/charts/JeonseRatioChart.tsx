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
  ReferenceLine,
} from 'recharts';
import { JeonseRatioDataItem } from '@/types/analysis';

interface JeonseRatioChartProps {
  data: JeonseRatioDataItem[];
}

export default function JeonseRatioChart({ data }: JeonseRatioChartProps) {
  const chartData = data.map((item) => ({
    region: item.region,
    전세가율: item.avg_jeonse_ratio,
    평균갭: Math.round(item.avg_gap / 10000),
  }));

  const getBarColor = (value: number) => {
    if (value >= 80) return '#ef4444';
    if (value >= 70) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        지역별 평균 전세가율
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
              value: '전세가율 (%)',
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
            formatter={(value: number, name: string) => {
              if (name === '전세가율') {
                return [`${value.toFixed(1)}%`, name];
              }
              return [`${value.toLocaleString('ko-KR')}억원`, name];
            }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <ReferenceLine
            y={80}
            stroke="#ef4444"
            strokeDasharray="3 3"
            label={{ value: '위험선 (80%)', position: 'right', fill: '#ef4444' }}
          />
          <ReferenceLine
            y={70}
            stroke="#f59e0b"
            strokeDasharray="3 3"
            label={{ value: '주의선 (70%)', position: 'right', fill: '#f59e0b' }}
          />
          <Bar
            dataKey="전세가율"
            fill="#3b82f6"
            name="전세가율"
            shape={(props: any) => {
              const { x, y, width, height, payload } = props;
              const color = getBarColor(payload.전세가율);
              return (
                <rect
                  x={x}
                  y={y}
                  width={width}
                  height={height}
                  fill={color}
                  rx={4}
                />
              );
            }}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
