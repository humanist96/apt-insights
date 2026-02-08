'use client';

import { useMemo } from 'react';
import Card from '@/components/ui/Card';
import { CollectionProgress } from '@/types/batch-collection';

interface CollectionProgressProps {
  progress: CollectionProgress;
  onCancel: () => void;
}

export default function CollectionProgressComponent({
  progress,
  onCancel,
}: CollectionProgressProps) {
  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  const calculateDuration = (start: string, end?: string) => {
    const startTime = new Date(start).getTime();
    const endTime = end ? new Date(end).getTime() : Date.now();
    const durationMs = endTime - startTime;
    const seconds = Math.floor(durationMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
      return `${minutes}분 ${remainingSeconds}초`;
    }
    return `${seconds}초`;
  };

  const totalSuccess = useMemo(() => {
    return progress.apiProgress.reduce((sum, api) => sum + api.successCount, 0);
  }, [progress.apiProgress]);

  const totalErrors = useMemo(() => {
    return progress.apiProgress.reduce((sum, api) => sum + api.errorCount, 0);
  }, [progress.apiProgress]);

  const statusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:bg-green-900/30 dark:text-green-400">
            완료
          </span>
        );
      case 'running':
        return (
          <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
            진행중
          </span>
        );
      case 'error':
        return (
          <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-800 dark:bg-red-900/30 dark:text-red-400">
            오류
          </span>
        );
      case 'cancelled':
        return (
          <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:bg-gray-700 dark:text-gray-400">
            취소됨
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:bg-gray-700 dark:text-gray-400">
            대기중
          </span>
        );
    }
  };

  return (
    <div className="space-y-4">
      <Card title="수집 진행 상황">
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                시작 시간: {formatTime(progress.startTime)}
              </div>
              {progress.endTime && (
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  종료 시간: {formatTime(progress.endTime)}
                </div>
              )}
              <div className="text-sm text-gray-500 dark:text-gray-400">
                경과 시간: {calculateDuration(progress.startTime, progress.endTime)}
              </div>
            </div>
            <div>{statusBadge(progress.status)}</div>
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                전체 진행률
              </span>
              <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                {(progress.overallProgress * 100).toFixed(1)}%
              </span>
            </div>
            <div className="h-4 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
              <div
                className="h-full rounded-full bg-blue-600 transition-all duration-300 dark:bg-blue-500"
                style={{ width: `${progress.overallProgress * 100}%` }}
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="rounded-lg bg-green-50 p-4 dark:bg-green-900/20">
              <div className="text-sm text-gray-600 dark:text-gray-400">성공</div>
              <div className="mt-1 text-2xl font-semibold text-green-600 dark:text-green-400">
                {totalSuccess}
              </div>
            </div>
            <div className="rounded-lg bg-red-50 p-4 dark:bg-red-900/20">
              <div className="text-sm text-gray-600 dark:text-gray-400">실패</div>
              <div className="mt-1 text-2xl font-semibold text-red-600 dark:text-red-400">
                {totalErrors}
              </div>
            </div>
            <div className="rounded-lg bg-blue-50 p-4 dark:bg-blue-900/20">
              <div className="text-sm text-gray-600 dark:text-gray-400">수집 레코드</div>
              <div className="mt-1 text-2xl font-semibold text-blue-600 dark:text-blue-400">
                {progress.totalRecords.toLocaleString()}
              </div>
            </div>
          </div>

          <div>
            <h4 className="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
              API별 진행 상황
            </h4>
            <div className="space-y-3">
              {progress.apiProgress.map((api) => {
                const progressPct = api.total > 0 ? (api.current / api.total) * 100 : 0;
                return (
                  <div
                    key={api.apiId}
                    className="rounded-lg border border-gray-200 p-4 dark:border-gray-700"
                  >
                    <div className="mb-2 flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-gray-900 dark:text-white">
                          {api.apiName}
                        </span>
                        {statusBadge(api.status)}
                      </div>
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {api.current} / {api.total}
                      </span>
                    </div>
                    {api.currentMonth && (
                      <div className="mb-2 text-xs text-gray-500 dark:text-gray-400">
                        현재: {api.currentMonth}
                      </div>
                    )}
                    <div className="mb-2 h-2 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
                      <div
                        className="h-full rounded-full bg-blue-600 transition-all duration-300 dark:bg-blue-500"
                        style={{ width: `${progressPct}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400">
                      <span>성공: {api.successCount}</span>
                      <span>실패: {api.errorCount}</span>
                    </div>
                    {api.errorMessage && (
                      <div className="mt-2 text-xs text-red-600 dark:text-red-400">
                        오류: {api.errorMessage}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {progress.status === 'running' && (
            <div className="flex justify-end">
              <button
                type="button"
                onClick={onCancel}
                className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:bg-red-500 dark:hover:bg-red-600"
              >
                수집 취소
              </button>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
