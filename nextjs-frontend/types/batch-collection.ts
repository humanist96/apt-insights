export interface ApiType {
  id: string;
  name: string;
  label: string;
  description: string;
}

export interface RegionOption {
  code: string;
  name: string;
}

export interface CollectionConfig {
  regions: string[];
  startMonth: string; // YYYYMM format
  endMonth: string; // YYYYMM format
  apis: string[];
}

export interface ApiProgress {
  apiId: string;
  apiName: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  current: number;
  total: number;
  successCount: number;
  errorCount: number;
  currentMonth?: string;
  errorMessage?: string;
}

export interface CollectionProgress {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'error' | 'cancelled';
  config: CollectionConfig;
  overallProgress: number;
  apiProgress: ApiProgress[];
  startTime: string;
  endTime?: string;
  estimatedEndTime?: string;
  totalRecords: number;
  message?: string;
}

export interface CollectionHistoryItem {
  id: string;
  startTime: string;
  endTime?: string;
  config: CollectionConfig;
  status: 'completed' | 'error' | 'running' | 'cancelled';
  totalRecords: number;
  successCount: number;
  errorCount: number;
  regionNames: string[];
  apiNames: string[];
  errorMessages?: string[];
}

export interface CollectionStatistics {
  totalCollections: number;
  successfulCollections: number;
  failedCollections: number;
  totalRecordsCollected: number;
  lastCollectionTime?: string;
  averageRecordsPerCollection: number;
}
