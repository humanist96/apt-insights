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
  Line,
  Legend,
  ReferenceLine,
} from 'recharts';
import { BargainSalesItem } from '@/types/analysis';

interface BargainSalesScatterProps {
  data: BargainSalesItem[];
}

export default function BargainSalesScatter({ data }: BargainSalesScatterProps) {
  const chartData = data.map((item) => ({
    ...item,
    expected: item.avg_price,
    actual: item.current_price,
    z: item.discount_pct,
  }));

  const getColor = (discountPct: number) => {
    if (discountPct >= 25) return '#dc2626';
    if (discountPct >= 20) return '#ea580c';
    if (discountPct >= 15) return '#f59e0b';
    return '#10b981';
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-semibold text-gray-900 dark:text-white">{data.apt_name}</p>
          <p className="text-sm text-gray-600 dark:text-gray-400">{data.region}</p>
          <div className="mt-2 space-y-1 text-sm">
            <p className="text-gray-900 dark:text-white">
              평균가: {(data.expected / 10000).toFixed(1)}억원
            </p>
            <p className="text-gray-900 dark:text-white">
              실거래가: {(data.actual / 10000).toFixed(1)}억원
            </p>
            <p className="text-red-600 dark:text-red-400 font-semibold">
              할인율: {data.discount_pct.toFixed(1)}%
            </p>
            <p className="text-blue-600 dark:text-blue-400">
              절감액: {(data.savings / 10000).toFixed(1)}억원
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  const maxPrice = Math.max(...data.map((d) => Math.max(d.avg_price, d.current_price)));
  const minPrice = Math.min(...data.map((d) => Math.min(d.avg_price, d.current_price)));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        시세 대비 거래가 분포
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        점의 크기는 할인율을 나타냅니다. 대각선 아래는 급매물 영역입니다.
      </p>
      <ResponsiveContainer width="100%" height={500}>
        <ScatterChart
          margin={{
            top: 20,
            right: 20,
            bottom: 20,
            left: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
          <XAxis
            type="number"
            dataKey="expected"
            name="평균 시세"
            unit="만원"
            domain={[Math.floor(minPrice * 0.9), Math.ceil(maxPrice * 1.1)]}
            tickFormatter={(value) => `${Math.round(value / 10000)}억`}
            className="text-gray-600 dark:text-gray-400"
          />
          <YAxis
            type="number"
            dataKey="actual"
            name="실거래가"
            unit="만원"
            domain={[Math.floor(minPrice * 0.9), Math.ceil(maxPrice * 1.1)]}
            tickFormatter={(value) => `${Math.round(value / 10000)}억`}
            className="text-gray-600 dark:text-gray-400"
          />
          <ZAxis type="number" dataKey="z" range={[50, 400]} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <ReferenceLine
            segment={[
              { x: minPrice, y: minPrice },
              { x: maxPrice, y: maxPrice },
            ]}
            stroke="#9ca3af"
            strokeDasharray="5 5"
            label={{ value: '정상가', position: 'insideTopRight' }}
          />
          <Scatter
            name="급매물"
            data={chartData}
            fill="#ef4444"
            shape={(props: any) => {
              const { cx, cy, payload } = props;
              const color = getColor(payload.discount_pct);
              return (
                <circle
                  cx={cx}
                  cy={cy}
                  r={Math.sqrt(payload.z) * 2}
                  fill={color}
                  fillOpacity={0.6}
                  stroke={color}
                  strokeWidth={2}
                />
              );
            }}
          />
        </ScatterChart>
      </ResponsiveContainer>
      <div className="mt-4 flex flex-wrap gap-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-red-600"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">초특급 (25% 이상)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-orange-600"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">특급 (20-25%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-amber-500"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">일반 (15-20%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-emerald-500"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">경미 (15% 미만)</span>
        </div>
      </div>
    </div>
  );
}
