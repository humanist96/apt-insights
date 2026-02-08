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
  Cell,
} from 'recharts';
import { ApartmentDataItem } from '@/types/analysis';

interface ApartmentBarChartProps {
  data: ApartmentDataItem[];
  onBarClick?: (apartment: ApartmentDataItem) => void;
  maxItems?: number;
}

export default function ApartmentBarChart({
  data,
  onBarClick,
  maxItems = 10,
}: ApartmentBarChartProps) {
  const chartData = data.slice(0, maxItems).map((apt) => ({
    name: apt.apt_name,
    평균가격: apt.avg_price ? Math.round(apt.avg_price / 10000) : 0,
    최고가: apt.max_price ? Math.round(apt.max_price / 10000) : 0,
    최저가: apt.min_price ? Math.round(apt.min_price / 10000) : 0,
    apt_data: apt,
  }));

  const formatYAxis = (value: number) => {
    return `${value}억`;
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload || !payload.length) return null;

    const data = payload[0].payload;

    return (
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-4">
        <p className="font-semibold text-gray-900 dark:text-white mb-2">{data.name}</p>
        <div className="space-y-1 text-sm">
          <div className="flex justify-between gap-4">
            <span className="text-blue-600 dark:text-blue-400">평균가격:</span>
            <span className="font-medium text-gray-900 dark:text-white">{data.평균가격}억원</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-green-600 dark:text-green-400">최고가:</span>
            <span className="font-medium text-gray-900 dark:text-white">{data.최고가}억원</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-orange-600 dark:text-orange-400">최저가:</span>
            <span className="font-medium text-gray-900 dark:text-white">{data.최저가}억원</span>
          </div>
        </div>
      </div>
    );
  };

  const handleClick = (data: any) => {
    if (onBarClick && data.apt_data) {
      onBarClick(data.apt_data);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        거래 활발 아파트 TOP {maxItems}
      </h3>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={100}
            tick={{ fill: 'currentColor' }}
            className="text-gray-600 dark:text-gray-400 text-xs"
          />
          <YAxis
            tickFormatter={formatYAxis}
            tick={{ fill: 'currentColor' }}
            className="text-gray-600 dark:text-gray-400"
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="square"
            formatter={(value) => (
              <span className="text-gray-700 dark:text-gray-300">{value}</span>
            )}
          />
          <Bar
            dataKey="평균가격"
            fill="#3b82f6"
            onClick={handleClick}
            cursor={onBarClick ? 'pointer' : 'default'}
          />
          <Bar
            dataKey="최고가"
            fill="#10b981"
            onClick={handleClick}
            cursor={onBarClick ? 'pointer' : 'default'}
          />
          <Bar
            dataKey="최저가"
            fill="#f97316"
            onClick={handleClick}
            cursor={onBarClick ? 'pointer' : 'default'}
          />
        </BarChart>
      </ResponsiveContainer>

      <p className="text-sm text-gray-600 dark:text-gray-400 mt-4 text-center">
        아파트별 가격 비교 (단위: 억원)
      </p>
    </div>
  );
}
