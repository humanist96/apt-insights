import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, PricePerAreaTrendAnalysis } from '@/types/analysis';
import { mockPricePerAreaTrend } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface UsePricePerAreaTrendParams {
  regionFilter?: string;
  startDate?: string;
  endDate?: string;
}

export function usePricePerAreaTrend(params?: UsePricePerAreaTrendParams) {
  return useQuery<ApiResponse<PricePerAreaTrendAnalysis>>({
    queryKey: ['price-per-area-trend', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        return mockPricePerAreaTrend;
      }

      const response = await apiClient.post<ApiResponse<PricePerAreaTrendAnalysis>>(
        '/api/v1/premium/price-per-area-trend',
        {
          region_filter: params?.regionFilter && params.regionFilter !== 'all'
            ? params.regionFilter
            : undefined,
          start_date: params?.startDate || undefined,
          end_date: params?.endDate || undefined,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
