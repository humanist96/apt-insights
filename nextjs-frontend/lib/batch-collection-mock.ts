import { CollectionHistoryItem, CollectionStatistics } from '@/types/batch-collection';

export const REGION_OPTIONS = [
  { code: '11110', name: '서울특별시 종로구' },
  { code: '11680', name: '서울특별시 강남구' },
  { code: '11650', name: '서울특별시 서초구' },
  { code: '11710', name: '서울특별시 송파구' },
  { code: '11740', name: '서울특별시 강동구' },
  { code: '41117', name: '경기도 수원시 영통구' },
  { code: '41113', name: '경기도 수원시 권선구' },
  { code: '41111', name: '경기도 수원시 장안구' },
  { code: '41115', name: '경기도 수원시 팔달구' },
  { code: '41131', name: '경기도 성남시 수정구' },
  { code: '41133', name: '경기도 성남시 중원구' },
  { code: '41135', name: '경기도 성남시 분당구' },
];

export const API_OPTIONS = [
  {
    id: 'api_01',
    name: 'API 01',
    label: '분양권전매',
    description: '분양권 전매 실거래가',
  },
  {
    id: 'api_02',
    name: 'API 02',
    label: '매매',
    description: '아파트 매매 실거래가',
  },
  {
    id: 'api_03',
    name: 'API 03',
    label: '매매 상세',
    description: '아파트 매매 실거래가 상세',
  },
  {
    id: 'api_04',
    name: 'API 04',
    label: '전월세',
    description: '아파트 전월세 실거래가',
  },
];

export const MOCK_COLLECTION_HISTORY: CollectionHistoryItem[] = [
  {
    id: 'col_001',
    startTime: '2025-02-07T14:30:00',
    endTime: '2025-02-07T14:45:00',
    config: {
      regions: ['11680', '11650'],
      startMonth: '202301',
      endMonth: '202312',
      apis: ['api_02', 'api_04'],
    },
    status: 'completed',
    totalRecords: 15420,
    successCount: 24,
    errorCount: 0,
    regionNames: ['서울특별시 강남구', '서울특별시 서초구'],
    apiNames: ['매매', '전월세'],
  },
  {
    id: 'col_002',
    startTime: '2025-02-06T10:15:00',
    endTime: '2025-02-06T10:35:00',
    config: {
      regions: ['11710'],
      startMonth: '202306',
      endMonth: '202312',
      apis: ['api_02', 'api_03', 'api_04'],
    },
    status: 'completed',
    totalRecords: 8932,
    successCount: 21,
    errorCount: 0,
    regionNames: ['서울특별시 송파구'],
    apiNames: ['매매', '매매 상세', '전월세'],
  },
  {
    id: 'col_003',
    startTime: '2025-02-05T16:20:00',
    endTime: '2025-02-05T16:28:00',
    config: {
      regions: ['41117', '41113'],
      startMonth: '202310',
      endMonth: '202312',
      apis: ['api_02'],
    },
    status: 'error',
    totalRecords: 2156,
    successCount: 5,
    errorCount: 1,
    regionNames: ['경기도 수원시 영통구', '경기도 수원시 권선구'],
    apiNames: ['매매'],
    errorMessages: ['API 호출 실패: 타임아웃 (202312)'],
  },
  {
    id: 'col_004',
    startTime: '2025-02-04T09:00:00',
    endTime: '2025-02-04T09:45:00',
    config: {
      regions: ['11110', '11680', '11650', '11710'],
      startMonth: '202301',
      endMonth: '202306',
      apis: ['api_01', 'api_02', 'api_03', 'api_04'],
    },
    status: 'completed',
    totalRecords: 42815,
    successCount: 96,
    errorCount: 0,
    regionNames: ['서울특별시 종로구', '서울특별시 강남구', '서울특별시 서초구', '서울특별시 송파구'],
    apiNames: ['분양권전매', '매매', '매매 상세', '전월세'],
  },
  {
    id: 'col_005',
    startTime: '2025-02-03T13:10:00',
    endTime: '2025-02-03T13:12:00',
    config: {
      regions: ['11680'],
      startMonth: '202312',
      endMonth: '202312',
      apis: ['api_02'],
    },
    status: 'cancelled',
    totalRecords: 0,
    successCount: 0,
    errorCount: 0,
    regionNames: ['서울특별시 강남구'],
    apiNames: ['매매'],
  },
];

export function getMockCollectionHistory(): CollectionHistoryItem[] {
  if (typeof window === 'undefined') {
    return MOCK_COLLECTION_HISTORY;
  }

  const storedHistory = localStorage.getItem('collectionHistory');
  if (storedHistory) {
    try {
      return JSON.parse(storedHistory);
    } catch {
      return MOCK_COLLECTION_HISTORY;
    }
  }
  return MOCK_COLLECTION_HISTORY;
}

export function saveMockCollectionHistory(history: CollectionHistoryItem[]): void {
  if (typeof window === 'undefined') {
    return;
  }
  localStorage.setItem('collectionHistory', JSON.stringify(history));
}

export function getMockCollectionStatistics(history: CollectionHistoryItem[]): CollectionStatistics {
  const totalCollections = history.length;
  const successfulCollections = history.filter((item) => item.status === 'completed').length;
  const failedCollections = history.filter((item) => item.status === 'error').length;
  const totalRecordsCollected = history.reduce((sum, item) => sum + item.totalRecords, 0);
  const lastCollectionTime = history.length > 0 ? history[0].startTime : undefined;
  const averageRecordsPerCollection = totalCollections > 0 ? totalRecordsCollected / totalCollections : 0;

  return {
    totalCollections,
    successfulCollections,
    failedCollections,
    totalRecordsCollected,
    lastCollectionTime,
    averageRecordsPerCollection,
  };
}

export function getRegionName(code: string): string {
  const region = REGION_OPTIONS.find((r) => r.code === code);
  return region ? region.name : code;
}

export function getApiName(apiId: string): string {
  const api = API_OPTIONS.find((a) => a.id === apiId);
  return api ? api.label : apiId;
}
