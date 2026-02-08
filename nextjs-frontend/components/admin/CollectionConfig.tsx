'use client';

import { useState, useEffect } from 'react';
import Card from '@/components/ui/Card';
import { CollectionConfig } from '@/types/batch-collection';
import { REGION_OPTIONS, API_OPTIONS } from '@/lib/batch-collection-mock';

interface CollectionConfigProps {
  onConfigChange: (config: CollectionConfig) => void;
  disabled?: boolean;
}

export default function CollectionConfigComponent({
  onConfigChange,
  disabled = false,
}: CollectionConfigProps) {
  const [selectedRegions, setSelectedRegions] = useState<string[]>([]);
  const [selectedApis, setSelectedApis] = useState<string[]>(['api_02', 'api_04']);
  const [startMonth, setStartMonth] = useState('202301');
  const [endMonth, setEndMonth] = useState('202312');
  const [errors, setErrors] = useState<string[]>([]);

  const currentYear = new Date().getFullYear();
  const currentMonth = new Date().getMonth() + 1;

  useEffect(() => {
    const newErrors: string[] = [];

    if (selectedRegions.length === 0) {
      newErrors.push('최소 1개 이상의 지역을 선택해주세요');
    }

    if (selectedApis.length === 0) {
      newErrors.push('최소 1개 이상의 API를 선택해주세요');
    }

    if (startMonth > endMonth) {
      newErrors.push('시작월이 종료월보다 큽니다');
    }

    setErrors(newErrors);

    if (newErrors.length === 0) {
      onConfigChange({
        regions: selectedRegions,
        startMonth,
        endMonth,
        apis: selectedApis,
      });
    }
  }, [selectedRegions, selectedApis, startMonth, endMonth, onConfigChange]);

  const handleSelectAllRegions = () => {
    if (selectedRegions.length === REGION_OPTIONS.length) {
      setSelectedRegions([]);
    } else {
      setSelectedRegions(REGION_OPTIONS.map((r) => r.code));
    }
  };

  const handleToggleRegion = (code: string) => {
    setSelectedRegions((prev) => {
      if (prev.includes(code)) {
        return prev.filter((c) => c !== code);
      }
      return [...prev, code];
    });
  };

  const handleToggleApi = (apiId: string) => {
    setSelectedApis((prev) => {
      if (prev.includes(apiId)) {
        return prev.filter((id) => id !== apiId);
      }
      return [...prev, apiId];
    });
  };

  return (
    <div className="space-y-6">
      <Card title="수집 설정">
        <div className="space-y-6">
          <div>
            <div className="mb-3 flex items-center justify-between">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                지역 선택
              </label>
              <button
                type="button"
                onClick={handleSelectAllRegions}
                disabled={disabled}
                className="text-sm text-blue-600 hover:text-blue-700 disabled:text-gray-400 dark:text-blue-400 dark:hover:text-blue-300"
              >
                {selectedRegions.length === REGION_OPTIONS.length
                  ? '전체 해제'
                  : '전체 선택'}
              </button>
            </div>
            <div className="grid grid-cols-1 gap-2 md:grid-cols-2 lg:grid-cols-3">
              {REGION_OPTIONS.map((region) => {
                const isSelected = selectedRegions.includes(region.code);
                return (
                  <label
                    key={region.code}
                    className={`flex cursor-pointer items-center rounded-lg border p-3 transition-colors ${
                      disabled
                        ? 'cursor-not-allowed opacity-50'
                        : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                    } ${
                      isSelected
                        ? 'border-blue-500 bg-blue-50 dark:border-blue-400 dark:bg-blue-900/20'
                        : 'border-gray-300 dark:border-gray-600'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => handleToggleRegion(region.code)}
                      disabled={disabled}
                      className="mr-3 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {region.name}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {region.code}
                      </div>
                    </div>
                  </label>
                );
              })}
            </div>
          </div>

          <div>
            <label className="mb-3 block text-sm font-medium text-gray-700 dark:text-gray-300">
              수집 기간
            </label>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <label className="mb-2 block text-sm text-gray-600 dark:text-gray-400">
                  시작월
                </label>
                <input
                  type="month"
                  value={`${startMonth.slice(0, 4)}-${startMonth.slice(4, 6)}`}
                  onChange={(e) => {
                    const value = e.target.value.replace('-', '');
                    setStartMonth(value);
                  }}
                  disabled={disabled}
                  min="202001"
                  max={`${currentYear}-${currentMonth.toString().padStart(2, '0')}`}
                  className="w-full rounded-lg border border-gray-300 p-2.5 text-sm focus:border-blue-500 focus:ring-blue-500 disabled:bg-gray-100 disabled:text-gray-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-blue-500 dark:focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="mb-2 block text-sm text-gray-600 dark:text-gray-400">
                  종료월
                </label>
                <input
                  type="month"
                  value={`${endMonth.slice(0, 4)}-${endMonth.slice(4, 6)}`}
                  onChange={(e) => {
                    const value = e.target.value.replace('-', '');
                    setEndMonth(value);
                  }}
                  disabled={disabled}
                  min="202001"
                  max={`${currentYear}-${currentMonth.toString().padStart(2, '0')}`}
                  className="w-full rounded-lg border border-gray-300 p-2.5 text-sm focus:border-blue-500 focus:ring-blue-500 disabled:bg-gray-100 disabled:text-gray-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:focus:border-blue-500 dark:focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="mb-3 block text-sm font-medium text-gray-700 dark:text-gray-300">
              수집 API 선택
            </label>
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              {API_OPTIONS.map((api) => {
                const isSelected = selectedApis.includes(api.id);
                return (
                  <label
                    key={api.id}
                    className={`flex cursor-pointer items-start rounded-lg border p-4 transition-colors ${
                      disabled
                        ? 'cursor-not-allowed opacity-50'
                        : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                    } ${
                      isSelected
                        ? 'border-blue-500 bg-blue-50 dark:border-blue-400 dark:bg-blue-900/20'
                        : 'border-gray-300 dark:border-gray-600'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => handleToggleApi(api.id)}
                      disabled={disabled}
                      className="mr-3 mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {api.name}: {api.label}
                      </div>
                      <div className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                        {api.description}
                      </div>
                    </div>
                  </label>
                );
              })}
            </div>
          </div>

          {errors.length > 0 && (
            <div className="rounded-lg bg-red-50 p-4 dark:bg-red-900/20">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                    설정 오류
                  </h3>
                  <div className="mt-2 text-sm text-red-700 dark:text-red-300">
                    <ul className="list-disc space-y-1 pl-5">
                      {errors.map((error, index) => (
                        <li key={index}>{error}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
