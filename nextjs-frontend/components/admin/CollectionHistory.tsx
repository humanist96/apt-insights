'use client';

import { useState } from 'react';
import Card from '@/components/ui/Card';
import { CollectionHistoryItem } from '@/types/batch-collection';

interface CollectionHistoryProps {
  history: CollectionHistoryItem[];
}

export default function CollectionHistory({ history }: CollectionHistoryProps) {
  const [selectedItem, setSelectedItem] = useState<CollectionHistoryItem | null>(null);

  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const calculateDuration = (start: string, end?: string) => {
    if (!end) return '-';
    const startTime = new Date(start).getTime();
    const endTime = new Date(end).getTime();
    const durationMs = endTime - startTime;
    const seconds = Math.floor(durationMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
      return `${minutes}분 ${remainingSeconds}초`;
    }
    return `${seconds}초`;
  };

  const statusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:bg-green-900/30 dark:text-green-400">
            성공
          </span>
        );
      case 'error':
        return (
          <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800 dark:bg-red-900/30 dark:text-red-400">
            실패
          </span>
        );
      case 'running':
        return (
          <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
            진행중
          </span>
        );
      case 'cancelled':
        return (
          <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:bg-gray-700 dark:text-gray-400">
            취소됨
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <>
      <Card title="수집 이력">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  수집 시간
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  지역
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  API
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  레코드
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  성공/실패
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  소요시간
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  상태
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
                  작업
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-900">
              {history.length === 0 ? (
                <tr>
                  <td
                    colSpan={8}
                    className="px-4 py-8 text-center text-sm text-gray-500 dark:text-gray-400"
                  >
                    수집 이력이 없습니다.
                  </td>
                </tr>
              ) : (
                history.map((item) => (
                  <tr
                    key={item.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-800"
                  >
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-900 dark:text-white">
                      {formatTime(item.startTime)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                      <div className="max-w-xs truncate">
                        {item.regionNames.join(', ')}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                      <div className="max-w-xs truncate">
                        {item.apiNames.join(', ')}
                      </div>
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-900 dark:text-white">
                      {item.totalRecords.toLocaleString()}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-900 dark:text-white">
                      <span className="text-green-600 dark:text-green-400">
                        {item.successCount}
                      </span>
                      {' / '}
                      <span className="text-red-600 dark:text-red-400">
                        {item.errorCount}
                      </span>
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-900 dark:text-white">
                      {calculateDuration(item.startTime, item.endTime)}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3">
                      {statusBadge(item.status)}
                    </td>
                    <td className="whitespace-nowrap px-4 py-3 text-sm">
                      <button
                        type="button"
                        onClick={() => setSelectedItem(item)}
                        className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
                      >
                        상세보기
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {selectedItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
          <div className="w-full max-w-2xl rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                수집 상세 정보
              </h3>
              <button
                type="button"
                onClick={() => setSelectedItem(null)}
                className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  수집 ID
                </label>
                <div className="mt-1 text-sm text-gray-900 dark:text-white">
                  {selectedItem.id}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  상태
                </label>
                <div className="mt-1">{statusBadge(selectedItem.status)}</div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    시작 시간
                  </label>
                  <div className="mt-1 text-sm text-gray-900 dark:text-white">
                    {formatTime(selectedItem.startTime)}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    종료 시간
                  </label>
                  <div className="mt-1 text-sm text-gray-900 dark:text-white">
                    {selectedItem.endTime
                      ? formatTime(selectedItem.endTime)
                      : '-'}
                  </div>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  수집 기간
                </label>
                <div className="mt-1 text-sm text-gray-900 dark:text-white">
                  {selectedItem.config.startMonth.slice(0, 4)}년{' '}
                  {selectedItem.config.startMonth.slice(4)}월 ~{' '}
                  {selectedItem.config.endMonth.slice(0, 4)}년{' '}
                  {selectedItem.config.endMonth.slice(4)}월
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  지역 ({selectedItem.regionNames.length}개)
                </label>
                <div className="mt-1 text-sm text-gray-900 dark:text-white">
                  {selectedItem.regionNames.join(', ')}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  API ({selectedItem.apiNames.length}개)
                </label>
                <div className="mt-1 text-sm text-gray-900 dark:text-white">
                  {selectedItem.apiNames.join(', ')}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="rounded-lg bg-blue-50 p-3 dark:bg-blue-900/20">
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    총 레코드
                  </div>
                  <div className="mt-1 text-lg font-semibold text-blue-600 dark:text-blue-400">
                    {selectedItem.totalRecords.toLocaleString()}
                  </div>
                </div>
                <div className="rounded-lg bg-green-50 p-3 dark:bg-green-900/20">
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    성공
                  </div>
                  <div className="mt-1 text-lg font-semibold text-green-600 dark:text-green-400">
                    {selectedItem.successCount}
                  </div>
                </div>
                <div className="rounded-lg bg-red-50 p-3 dark:bg-red-900/20">
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    실패
                  </div>
                  <div className="mt-1 text-lg font-semibold text-red-600 dark:text-red-400">
                    {selectedItem.errorCount}
                  </div>
                </div>
              </div>

              {selectedItem.errorMessages && selectedItem.errorMessages.length > 0 && (
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    오류 메시지
                  </label>
                  <div className="mt-1 space-y-1">
                    {selectedItem.errorMessages.map((error, index) => (
                      <div
                        key={index}
                        className="text-sm text-red-600 dark:text-red-400"
                      >
                        {error}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedItem(null)}
                className="rounded-lg bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 dark:bg-gray-500 dark:hover:bg-gray-600"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
