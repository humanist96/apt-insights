'use client';

import { useState, useEffect } from 'react';
import { DetailDataFilters as Filters } from '@/types/analysis';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';

interface DetailDataFiltersProps {
  filters: Filters;
  onChange: (filters: Filters) => void;
}

export default function DetailDataFilters({
  filters,
  onChange,
}: DetailDataFiltersProps) {
  const [localFilters, setLocalFilters] = useState<Filters>(filters);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const regions = [
    '강남구',
    '서초구',
    '송파구',
    '마포구',
    '용산구',
    '영등포구',
    '양천구',
    '광진구',
  ];

  const transactionTypes = ['매매', '전세', '월세'];

  const handleRegionToggle = (region: string) => {
    const updatedRegions = localFilters.regions.includes(region)
      ? localFilters.regions.filter((r) => r !== region)
      : [...localFilters.regions, region];

    setLocalFilters({ ...localFilters, regions: updatedRegions });
  };

  const handleTransactionTypeToggle = (type: string) => {
    const updatedTypes = localFilters.transactionTypes.includes(type)
      ? localFilters.transactionTypes.filter((t) => t !== type)
      : [...localFilters.transactionTypes, type];

    setLocalFilters({ ...localFilters, transactionTypes: updatedTypes });
  };

  const validateFilters = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (
      localFilters.priceMin !== undefined &&
      localFilters.priceMax !== undefined &&
      localFilters.priceMin > localFilters.priceMax
    ) {
      newErrors.price = '최소 가격이 최대 가격보다 클 수 없습니다';
    }

    if (
      localFilters.areaMin !== undefined &&
      localFilters.areaMax !== undefined &&
      localFilters.areaMin > localFilters.areaMax
    ) {
      newErrors.area = '최소 면적이 최대 면적보다 클 수 없습니다';
    }

    if (
      localFilters.floorMin !== undefined &&
      localFilters.floorMax !== undefined &&
      localFilters.floorMin > localFilters.floorMax
    ) {
      newErrors.floor = '최소 층수가 최대 층수보다 클 수 없습니다';
    }

    if (
      localFilters.dateStart &&
      localFilters.dateEnd &&
      localFilters.dateStart > localFilters.dateEnd
    ) {
      newErrors.date = '시작 날짜가 종료 날짜보다 클 수 없습니다';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleApply = () => {
    if (validateFilters()) {
      onChange(localFilters);
    }
  };

  const handleReset = () => {
    const resetFilters: Filters = {
      regions: [],
      transactionTypes: [],
      searchQuery: '',
    };
    setLocalFilters(resetFilters);
    onChange(resetFilters);
    setErrors({});
  };

  return (
    <Card className="mb-6">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            필터 설정
          </h3>
        </div>

        {/* Region Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            지역 (다중 선택)
          </label>
          <div className="flex flex-wrap gap-2">
            {regions.map((region) => (
              <button
                key={region}
                onClick={() => handleRegionToggle(region)}
                className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
                  localFilters.regions.includes(region)
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:border-blue-500'
                }`}
              >
                {region}
              </button>
            ))}
          </div>
        </div>

        {/* Date Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              시작 날짜
            </label>
            <input
              type="date"
              value={localFilters.dateStart || ''}
              onChange={(e) =>
                setLocalFilters({ ...localFilters, dateStart: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              종료 날짜
            </label>
            <input
              type="date"
              value={localFilters.dateEnd || ''}
              onChange={(e) =>
                setLocalFilters({ ...localFilters, dateEnd: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        {errors.date && (
          <p className="text-sm text-red-600 dark:text-red-400">{errors.date}</p>
        )}

        {/* Price Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최소 가격 (만원)
            </label>
            <input
              type="number"
              value={localFilters.priceMin || ''}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  priceMin: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              placeholder="0"
              min="0"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최대 가격 (만원)
            </label>
            <input
              type="number"
              value={localFilters.priceMax || ''}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  priceMax: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              placeholder="무제한"
              min="0"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        {errors.price && (
          <p className="text-sm text-red-600 dark:text-red-400">{errors.price}</p>
        )}

        {/* Area Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최소 면적 (㎡)
            </label>
            <input
              type="number"
              value={localFilters.areaMin || ''}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  areaMin: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              placeholder="0"
              min="0"
              step="0.1"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최대 면적 (㎡)
            </label>
            <input
              type="number"
              value={localFilters.areaMax || ''}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  areaMax: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              placeholder="무제한"
              min="0"
              step="0.1"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        {errors.area && (
          <p className="text-sm text-red-600 dark:text-red-400">{errors.area}</p>
        )}

        {/* Floor Range */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최소 층수
            </label>
            <input
              type="number"
              value={localFilters.floorMin || ''}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  floorMin: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              placeholder="0"
              min="0"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              최대 층수
            </label>
            <input
              type="number"
              value={localFilters.floorMax || ''}
              onChange={(e) =>
                setLocalFilters({
                  ...localFilters,
                  floorMax: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              placeholder="무제한"
              min="0"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        {errors.floor && (
          <p className="text-sm text-red-600 dark:text-red-400">{errors.floor}</p>
        )}

        {/* Transaction Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            거래 유형
          </label>
          <div className="flex gap-3">
            {transactionTypes.map((type) => (
              <button
                key={type}
                onClick={() => handleTransactionTypeToggle(type)}
                className={`px-6 py-2 rounded-lg border text-sm font-medium transition-colors ${
                  localFilters.transactionTypes.includes(type)
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 hover:border-blue-500'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <Button onClick={handleApply} variant="primary" className="flex-1">
            필터 적용
          </Button>
          <Button onClick={handleReset} variant="secondary" className="flex-1">
            초기화
          </Button>
        </div>
      </div>
    </Card>
  );
}
