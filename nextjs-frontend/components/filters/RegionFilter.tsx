'use client';

interface RegionFilterProps {
  value?: string;
  onChange: (value: string) => void;
}

const regions = [
  { value: 'all', label: '전체 지역' },
  { value: '강남구', label: '강남구' },
  { value: '서초구', label: '서초구' },
  { value: '송파구', label: '송파구' },
  { value: '마포구', label: '마포구' },
  { value: '용산구', label: '용산구' },
  { value: '영등포구', label: '영등포구' },
  { value: '양천구', label: '양천구' },
  { value: '광진구', label: '광진구' },
];

export default function RegionFilter({ value = 'all', onChange }: RegionFilterProps) {
  return (
    <div className="w-full sm:w-64">
      <label
        htmlFor="region-filter"
        className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
      >
        지역 선택
      </label>
      <select
        id="region-filter"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
      >
        {regions.map((region) => (
          <option key={region.value} value={region.value}>
            {region.label}
          </option>
        ))}
      </select>
    </div>
  );
}
