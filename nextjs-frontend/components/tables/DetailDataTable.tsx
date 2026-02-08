'use client';

import { useState } from 'react';
import { DetailDataItem } from '@/types/analysis';
import Card from '@/components/ui/Card';

type SortField = 'apt_name' | 'region' | 'deal_date' | 'deal_amount' | 'area' | 'floor' | 'build_year' | 'transaction_type';
type SortOrder = 'asc' | 'desc';

interface DetailDataTableProps {
  data: DetailDataItem[];
  currentPage: number;
  totalPages: number;
  totalCount: number;
  onPageChange: (page: number) => void;
}

interface ColumnVisibility {
  region: boolean;
  area: boolean;
  floor: boolean;
  build_year: boolean;
  transaction_type: boolean;
}

export default function DetailDataTable({
  data,
  currentPage,
  totalPages,
  totalCount,
  onPageChange,
}: DetailDataTableProps) {
  const [sortField, setSortField] = useState<SortField>('deal_date');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');
  const [columnVisibility, setColumnVisibility] = useState<ColumnVisibility>({
    region: true,
    area: true,
    floor: true,
    build_year: true,
    transaction_type: true,
  });
  const [showColumnToggle, setShowColumnToggle] = useState(false);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    let aValue = a[sortField];
    let bValue = b[sortField];

    if (typeof aValue === 'string') {
      aValue = aValue.toLowerCase();
    }
    if (typeof bValue === 'string') {
      bValue = bValue.toLowerCase();
    }

    if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) {
      return (
        <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
        </svg>
      );
    }
    return sortOrder === 'asc' ? (
      <svg className="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
      </svg>
    ) : (
      <svg className="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
      </svg>
    );
  };

  const toggleColumn = (column: keyof ColumnVisibility) => {
    setColumnVisibility({
      ...columnVisibility,
      [column]: !columnVisibility[column],
    });
  };

  return (
    <Card>
      <div className="space-y-4">
        {/* Header */}
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            거래 데이터 ({totalCount.toLocaleString('ko-KR')}건)
          </h3>
          <div className="relative">
            <button
              onClick={() => setShowColumnToggle(!showColumnToggle)}
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              열 표시/숨김
            </button>
            {showColumnToggle && (
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10">
                <div className="p-3 space-y-2">
                  {Object.entries(columnVisibility).map(([key, value]) => (
                    <label key={key} className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value}
                        onChange={() => toggleColumn(key as keyof ColumnVisibility)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">
                        {key === 'region' && '지역'}
                        {key === 'area' && '면적'}
                        {key === 'floor' && '층'}
                        {key === 'build_year' && '건축년도'}
                        {key === 'transaction_type' && '거래유형'}
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50 dark:bg-gray-900">
                <th
                  onClick={() => handleSort('apt_name')}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <div className="flex items-center gap-1">
                    아파트명
                    <SortIcon field="apt_name" />
                  </div>
                </th>
                {columnVisibility.region && (
                  <th
                    onClick={() => handleSort('region')}
                    className="px-4 py-3 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    <div className="flex items-center gap-1">
                      지역
                      <SortIcon field="region" />
                    </div>
                  </th>
                )}
                <th
                  onClick={() => handleSort('deal_date')}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <div className="flex items-center gap-1">
                    거래일
                    <SortIcon field="deal_date" />
                  </div>
                </th>
                <th
                  onClick={() => handleSort('deal_amount')}
                  className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <div className="flex items-center justify-end gap-1">
                    거래가격 (만원)
                    <SortIcon field="deal_amount" />
                  </div>
                </th>
                {columnVisibility.area && (
                  <th
                    onClick={() => handleSort('area')}
                    className="px-4 py-3 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    <div className="flex items-center justify-end gap-1">
                      면적 (㎡)
                      <SortIcon field="area" />
                    </div>
                  </th>
                )}
                {columnVisibility.floor && (
                  <th
                    onClick={() => handleSort('floor')}
                    className="px-4 py-3 text-center text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    <div className="flex items-center justify-center gap-1">
                      층
                      <SortIcon field="floor" />
                    </div>
                  </th>
                )}
                {columnVisibility.build_year && (
                  <th
                    onClick={() => handleSort('build_year')}
                    className="px-4 py-3 text-center text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    <div className="flex items-center justify-center gap-1">
                      건축년도
                      <SortIcon field="build_year" />
                    </div>
                  </th>
                )}
                {columnVisibility.transaction_type && (
                  <th
                    onClick={() => handleSort('transaction_type')}
                    className="px-4 py-3 text-center text-xs font-medium text-gray-700 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
                  >
                    <div className="flex items-center justify-center gap-1">
                      거래유형
                      <SortIcon field="transaction_type" />
                    </div>
                  </th>
                )}
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {sortedData.map((item) => (
                <tr
                  key={item.id}
                  className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                    {item.apt_name}
                  </td>
                  {columnVisibility.region && (
                    <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                      {item.region}
                    </td>
                  )}
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {item.deal_date}
                  </td>
                  <td className="px-4 py-3 text-sm text-right font-medium text-gray-900 dark:text-white">
                    {item.deal_amount.toLocaleString('ko-KR')}
                  </td>
                  {columnVisibility.area && (
                    <td className="px-4 py-3 text-sm text-right text-gray-600 dark:text-gray-400">
                      {item.area.toLocaleString('ko-KR', {
                        minimumFractionDigits: 1,
                        maximumFractionDigits: 1,
                      })}
                    </td>
                  )}
                  {columnVisibility.floor && (
                    <td className="px-4 py-3 text-sm text-center text-gray-600 dark:text-gray-400">
                      {item.floor}층
                    </td>
                  )}
                  {columnVisibility.build_year && (
                    <td className="px-4 py-3 text-sm text-center text-gray-600 dark:text-gray-400">
                      {item.build_year}년
                    </td>
                  )}
                  {columnVisibility.transaction_type && (
                    <td className="px-4 py-3 text-sm text-center">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          item.transaction_type === '매매'
                            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                            : item.transaction_type === '전세'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                        }`}
                      >
                        {item.transaction_type}
                      </span>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              페이지 {currentPage} / {totalPages}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => onPageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                이전
              </button>
              <button
                onClick={() => onPageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                다음
              </button>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
}
