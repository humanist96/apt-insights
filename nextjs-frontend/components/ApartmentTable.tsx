'use client';

import { useState } from 'react';
import { ApartmentDataItem } from '@/types/analysis';

interface ApartmentTableProps {
  data: ApartmentDataItem[];
  onSelectApartment?: (apartment: ApartmentDataItem) => void;
}

type SortField = 'count' | 'avg_price' | 'max_price' | 'min_price' | 'avg_price_per_area';
type SortDirection = 'asc' | 'desc';

export default function ApartmentTable({ data, onSelectApartment }: ApartmentTableProps) {
  const [sortField, setSortField] = useState<SortField>('count');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((prev) => (prev === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    let aValue = 0;
    let bValue = 0;

    switch (sortField) {
      case 'count':
        aValue = a.count;
        bValue = b.count;
        break;
      case 'avg_price':
        aValue = a.avg_price || 0;
        bValue = b.avg_price || 0;
        break;
      case 'max_price':
        aValue = a.max_price || 0;
        bValue = b.max_price || 0;
        break;
      case 'min_price':
        aValue = a.min_price || 0;
        bValue = b.min_price || 0;
        break;
      case 'avg_price_per_area':
        aValue = a.avg_price_per_area || 0;
        bValue = b.avg_price_per_area || 0;
        break;
    }

    return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
  });

  const displayedData = sortedData.slice(0, 100);

  const formatPrice = (price?: number) => {
    if (!price) return '-';
    return `${(price / 10000).toLocaleString('ko-KR', { maximumFractionDigits: 0 })}억원`;
  };

  const formatPricePerArea = (price?: number) => {
    if (!price) return '-';
    return `${price.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}만원`;
  };

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) {
      return <span className="text-gray-400">↕</span>;
    }
    return <span>{sortDirection === 'asc' ? '↑' : '↓'}</span>;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                아파트명
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                지역
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                onClick={() => handleSort('count')}
              >
                거래건수 <SortIcon field="count" />
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                onClick={() => handleSort('avg_price')}
              >
                평균가격 <SortIcon field="avg_price" />
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                onClick={() => handleSort('max_price')}
              >
                최고가 <SortIcon field="max_price" />
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                onClick={() => handleSort('min_price')}
              >
                최저가 <SortIcon field="min_price" />
              </th>
              <th
                className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                onClick={() => handleSort('avg_price_per_area')}
              >
                평당가 <SortIcon field="avg_price_per_area" />
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {displayedData.map((apartment, index) => (
              <tr
                key={`${apartment.apt_name}-${apartment.region}-${index}`}
                onClick={() => onSelectApartment?.(apartment)}
                className={
                  onSelectApartment
                    ? 'cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors'
                    : ''
                }
              >
                <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">
                  {apartment.apt_name}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                  {apartment.region || '-'}
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                  {apartment.count.toLocaleString('ko-KR')}
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                  {formatPrice(apartment.avg_price)}
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-600 dark:text-gray-400">
                  {formatPrice(apartment.max_price)}
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-600 dark:text-gray-400">
                  {formatPrice(apartment.min_price)}
                </td>
                <td className="px-4 py-3 text-sm text-right text-gray-900 dark:text-white">
                  {formatPricePerArea(apartment.avg_price_per_area)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {data.length > 100 && (
        <div className="px-4 py-3 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            상위 100개만 표시됩니다. 전체 {data.length.toLocaleString('ko-KR')}개 중
          </p>
        </div>
      )}

      {displayedData.length === 0 && (
        <div className="px-4 py-12 text-center">
          <p className="text-gray-600 dark:text-gray-400">표시할 데이터가 없습니다</p>
        </div>
      )}
    </div>
  );
}
