import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, PricePerAreaAnalysis } from '@/types/analysis';
import { mockPricePerArea } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface UsePricePerAreaParams {
  regionFilter?: string;
  startDate?: string;
  endDate?: string;
}

export function usePricePerArea(params?: UsePricePerAreaParams) {
  return useQuery<ApiResponse<PricePerAreaAnalysis>>({
    queryKey: ['price-per-area', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        return mockPricePerArea;
      }

      const response = await apiClient.post<ApiResponse<PricePerAreaAnalysis>>(
        '/api/v1/premium/price-per-area',
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
