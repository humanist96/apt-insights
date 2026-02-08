import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, PriceTrendAnalysis } from '@/types/analysis';
import { mockPriceTrend } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface PriceTrendParams {
  startDate?: string;
  endDate?: string;
  regionFilter?: string;
  groupBy?: 'month' | 'quarter';
}

export function usePriceTrend(params: PriceTrendParams = {}) {
  return useQuery<ApiResponse<PriceTrendAnalysis>>({
    queryKey: ['price-trend', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        return mockPriceTrend;
      }

      const response = await apiClient.post<ApiResponse<PriceTrendAnalysis>>(
        '/api/v1/analysis/price-trend',
        {
          start_date: params.startDate,
          end_date: params.endDate,
          region_filter: params.regionFilter,
          group_by: params.groupBy || 'month',
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
