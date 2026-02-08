'use client';

import { useState, useEffect } from 'react';

interface AreaBinsSelectorProps {
  bins: number[];
  onChange: (bins: number[]) => void;
}

const DEFAULT_BINS = [50, 60, 85, 100, 135];

export default function AreaBinsSelector({ bins, onChange }: AreaBinsSelectorProps) {
  const [inputValues, setInputValues] = useState<string[]>(
    bins.length > 0 ? bins.map(String) : DEFAULT_BINS.map(String)
  );
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (bins.length > 0) {
      setInputValues(bins.map(String));
    }
  }, [bins]);

  const handleInputChange = (index: number, value: string) => {
    const newInputValues = [...inputValues];
    newInputValues[index] = value;
    setInputValues(newInputValues);
    validateAndUpdate(newInputValues);
  };

  const validateAndUpdate = (values: string[]) => {
    const numbers = values
      .map((v) => parseFloat(v))
      .filter((n) => !isNaN(n) && n > 0);

    if (numbers.length !== values.length) {
      setError('모든 값은 양수여야 합니다');
      return;
    }

    const sorted = [...numbers].sort((a, b) => a - b);
    if (JSON.stringify(sorted) !== JSON.stringify(numbers)) {
      setError('면적 구간은 오름차순으로 입력해야 합니다');
      return;
    }

    setError('');
    onChange(numbers);
  };

  const addBin = () => {
    const lastValue = inputValues.length > 0 ? parseFloat(inputValues[inputValues.length - 1]) : 0;
    const newValue = lastValue + 10;
    const newInputValues = [...inputValues, String(newValue)];
    setInputValues(newInputValues);
    validateAndUpdate(newInputValues);
  };

  const removeBin = (index: number) => {
    if (inputValues.length <= 2) {
      setError('최소 2개의 구간이 필요합니다');
      return;
    }
    const newInputValues = inputValues.filter((_, i) => i !== index);
    setInputValues(newInputValues);
    validateAndUpdate(newInputValues);
  };

  const resetToDefault = () => {
    const defaultValues = DEFAULT_BINS.map(String);
    setInputValues(defaultValues);
    validateAndUpdate(defaultValues);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          면적 구간 설정 (㎡)
        </label>
        <button
          onClick={resetToDefault}
          className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
        >
          기본값으로 초기화
        </button>
      </div>

      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-sm text-gray-600 dark:text-gray-400">0 ~</span>
        {inputValues.map((value, index) => (
          <div key={index} className="flex items-center gap-2">
            <input
              type="number"
              value={value}
              onChange={(e) => handleInputChange(index, e.target.value)}
              className="w-20 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              min="0"
              step="1"
            />
            {index < inputValues.length - 1 && (
              <span className="text-sm text-gray-600 dark:text-gray-400">~</span>
            )}
            <button
              onClick={() => removeBin(index)}
              className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 disabled:opacity-50"
              disabled={inputValues.length <= 2}
              title="구간 삭제"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        ))}
        <span className="text-sm text-gray-600 dark:text-gray-400">~ ∞</span>
        <button
          onClick={addBin}
          className="ml-2 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          title="구간 추가"
        >
          + 추가
        </button>
      </div>

      {error && (
        <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
      )}

      <div className="text-xs text-gray-500 dark:text-gray-400">
        <p>기본 구간: 소형(~50㎡), 중소형(50-60㎡), 중형(60-85㎡), 중대형(85-100㎡), 대형(100-135㎡), 초대형(135㎡~)</p>
      </div>
    </div>
  );
}
