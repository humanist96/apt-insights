'use client';

import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
} from 'recharts';
import { ApartmentDataItem } from '@/types/analysis';

interface ApartmentScatterChartProps {
  data: ApartmentDataItem[];
  onPointClick?: (apartment: ApartmentDataItem) => void;
}

export default function ApartmentScatterChart({
  data,
  onPointClick,
}: ApartmentScatterChartProps) {
  const chartData = data
    .filter((apt) => apt.avg_price_per_area && apt.avg_price)
    .map((apt) => ({
      x: apt.avg_price_per_area || 0,
      y: apt.avg_price ? Math.round(apt.avg_price / 10000) : 0,
      z: apt.count,
      name: apt.apt_name,
      region: apt.region || 'N/A',
      apt_data: apt,
    }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload || !payload.length) return null;

    const data = payload[0].payload;

    return (
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-4">
        <p className="font-semibold text-gray-900 dark:text-white mb-2">{data.name}</p>
        <div className="space-y-1 text-sm">
          <div className="flex justify-between gap-4">
            <span className="text-gray-600 dark:text-gray-400">지역:</span>
            <span className="font-medium text-gray-900 dark:text-white">{data.region}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-gray-600 dark:text-gray-400">평균가격:</span>
            <span className="font-medium text-gray-900 dark:text-white">{data.y}억원</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-gray-600 dark:text-gray-400">평당가:</span>
            <span className="font-medium text-gray-900 dark:text-white">
              {data.x.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}만원
            </span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-gray-600 dark:text-gray-400">거래건수:</span>
            <span className="font-medium text-gray-900 dark:text-white">{data.z}건</span>
          </div>
        </div>
      </div>
    );
  };

  const handleClick = (data: any) => {
    if (onPointClick && data.apt_data) {
      onPointClick(data.apt_data);
    }
  };

  const formatYAxis = (value: number) => {
    return `${value}억`;
  };

  const formatXAxis = (value: number) => {
    return `${value}`;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        평당가 vs 평균가격 분포
      </h3>

      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
          <XAxis
            type="number"
            dataKey="x"
            name="평당가"
            tickFormatter={formatXAxis}
            tick={{ fill: 'currentColor' }}
            className="text-gray-600 dark:text-gray-400"
            label={{
              value: '평당가 (만원/㎡)',
              position: 'insideBottom',
              offset: -10,
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="평균가격"
            tickFormatter={formatYAxis}
            tick={{ fill: 'currentColor' }}
            className="text-gray-600 dark:text-gray-400"
            label={{
              value: '평균가격 (억원)',
              angle: -90,
              position: 'insideLeft',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <ZAxis type="number" dataKey="z" range={[50, 400]} name="거래건수" />
          <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
          <Scatter
            name="아파트"
            data={chartData}
            fill="#3b82f6"
            fillOpacity={0.6}
            onClick={handleClick}
            cursor={onPointClick ? 'pointer' : 'default'}
          />
        </ScatterChart>
      </ResponsiveContainer>

      <p className="text-sm text-gray-600 dark:text-gray-400 mt-4 text-center">
        버블 크기는 거래건수를 나타냅니다
      </p>
    </div>
  );
}
