'use client';

import { useState } from 'react';
import { BargainSalesItem } from '@/types/analysis';

interface BargainSalesTableProps {
  data: BargainSalesItem[];
}

type SortField = 'discount_pct' | 'savings' | 'current_price' | 'deal_date';
type SortOrder = 'asc' | 'desc';

export default function BargainSalesTable({ data }: BargainSalesTableProps) {
  const [sortField, setSortField] = useState<SortField>('discount_pct');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    const multiplier = sortOrder === 'asc' ? 1 : -1;
    const aVal = a[sortField];
    const bVal = b[sortField];
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return (aVal - bVal) * multiplier;
    }
    return String(aVal).localeCompare(String(bVal)) * multiplier;
  });

  const getDiscountBadge = (discountPct: number) => {
    if (discountPct >= 25) {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
          초특급
        </span>
      );
    }
    if (discountPct >= 20) {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300">
          특급
        </span>
      );
    }
    if (discountPct >= 15) {
      return (
        <span className="px-2 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300">
          일반
        </span>
      );
    }
    return (
      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300">
        경미
      </span>
    );
  };

  const SortButton = ({ field, label }: { field: SortField; label: string }) => {
    return (
      <button
        onClick={() => handleSort(field)}
        className="flex items-center gap-1 hover:text-blue-600 dark:hover:text-blue-400"
      >
        {label}
        {sortField === field && (
          <span className="text-xs">{sortOrder === 'asc' ? '▲' : '▼'}</span>
        )}
      </button>
    );
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          급매물 상세 목록
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          컬럼 헤더를 클릭하여 정렬할 수 있습니다.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                등급
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                아파트
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                지역
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                <SortButton field="discount_pct" label="할인율" />
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                <SortButton field="current_price" label="실거래가" />
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                평균시세
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                <SortButton field="savings" label="절감액" />
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                면적
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                층
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                <SortButton field="deal_date" label="거래일" />
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {sortedData.map((item, idx) => (
              <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                <td className="px-4 py-3 whitespace-nowrap">
                  {getDiscountBadge(item.discount_pct)}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                  {item.apt_name}
                </td>
                <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                  {item.region}
                </td>
                <td className="px-4 py-3 text-sm text-right text-red-600 dark:text-red-400 font-semibold">
                  {item.discount_pct.toFixed(1)}%
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                  {Math.round(item.current_price / 10000).toLocaleString('ko-KR')}억
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-500 dark:text-gray-400">
                  {Math.round(item.avg_price / 10000).toLocaleString('ko-KR')}억
                </td>
                <td className="px-4 py-3 text-sm text-right text-blue-600 dark:text-blue-400 font-semibold">
                  {Math.round(item.savings / 10000).toLocaleString('ko-KR')}억
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                  {item.area.toFixed(1)}㎡
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                  {item.floor}층
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-500 dark:text-gray-400">
                  {item.deal_date}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
