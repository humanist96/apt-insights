'use client';

import { useQuery } from '@tanstack/react-query';
import { ApiResponse, AreaAnalysis } from '@/types/analysis';
import { mockByArea } from '@/lib/mock-data';

interface UseByAreaParams {
  region?: string;
  startDate?: string;
  endDate?: string;
  bins?: number[];
}

const fetchByArea = async (params: UseByAreaParams): Promise<ApiResponse<AreaAnalysis>> => {
  const queryParams = new URLSearchParams();

  if (params.region && params.region !== 'all') {
    queryParams.append('region', params.region);
  }
  if (params.startDate) {
    queryParams.append('start_date', params.startDate);
  }
  if (params.endDate) {
    queryParams.append('end_date', params.endDate);
  }
  if (params.bins && params.bins.length > 0) {
    queryParams.append('bins', params.bins.join(','));
  }

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const url = `${apiUrl}/api/v1/analysis/by-area${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        bins: params.bins,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch area analysis data');
    }

    return await response.json();
  } catch (error) {
    return mockByArea;
  }
};

export const useByArea = (params: UseByAreaParams = {}) => {
  return useQuery({
    queryKey: ['byArea', params],
    queryFn: () => fetchByArea(params),
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });
};
