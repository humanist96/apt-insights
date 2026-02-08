'use client';

import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend,
  ZAxis,
} from 'recharts';
import { GapInvestmentOpportunity } from '@/types/analysis';

interface GapInvestmentScatterProps {
  data: GapInvestmentOpportunity[];
}

export default function GapInvestmentScatter({ data }: GapInvestmentScatterProps) {
  const chartData = data.map((item) => ({
    전세가: Math.round(item.avg_jeonse_price / 10000),
    매매가: Math.round(item.avg_trade_price / 10000),
    갭: Math.round(item.gap / 10000),
    전세가율: item.jeonse_ratio,
    아파트: item.apt_name,
    지역: item.region,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-semibold text-gray-900 dark:text-white mb-2">
            {data.아파트}
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            지역: {data.지역}
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            매매가: {data.매매가.toLocaleString('ko-KR')}억원
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            전세가: {data.전세가.toLocaleString('ko-KR')}억원
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
            갭: {data.갭.toLocaleString('ko-KR')}억원
          </p>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            전세가율: {data.전세가율.toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        매매가 vs 전세가 분포
      </h3>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        버블 크기는 갭 금액을 나타냅니다
      </p>
      <ResponsiveContainer width="100%" height={500}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-600" />
          <XAxis
            type="number"
            dataKey="전세가"
            name="전세가"
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '전세가 (억원)',
              position: 'insideBottom',
              offset: -10,
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <YAxis
            type="number"
            dataKey="매매가"
            name="매매가"
            className="text-xs fill-gray-700 dark:fill-gray-300"
            label={{
              value: '매매가 (억원)',
              angle: -90,
              position: 'insideLeft',
              className: 'fill-gray-700 dark:fill-gray-300',
            }}
          />
          <ZAxis type="number" dataKey="갭" range={[100, 1000]} name="갭" />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <ReferenceLine
            segment={[
              { x: 0, y: 0 },
              { x: 300, y: 375 },
            ]}
            stroke="#ef4444"
            strokeDasharray="5 5"
            label={{ value: '전세가율 80%', position: 'insideTopRight', fill: '#ef4444' }}
          />
          <Scatter
            name="아파트"
            data={chartData}
            fill="#3b82f6"
            fillOpacity={0.6}
            shape={(props: any) => {
              const { cx, cy, payload } = props;
              const ratio = payload.전세가율;
              const color = ratio >= 80 ? '#ef4444' : ratio >= 70 ? '#f59e0b' : '#10b981';
              return (
                <circle
                  cx={cx}
                  cy={cy}
                  r={Math.sqrt(payload.갭) * 2}
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
    </div>
  );
}
