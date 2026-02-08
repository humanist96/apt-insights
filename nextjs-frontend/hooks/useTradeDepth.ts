import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, TradeDepthAnalysis } from '@/types/analysis';
import { mockTradeDepth } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

export function useTradeDepth(regionFilter?: string, dateRange?: { start: string; end: string }) {
  return useQuery<ApiResponse<TradeDepthAnalysis>>({
    queryKey: ['trade-depth', regionFilter, dateRange],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));
        return mockTradeDepth;
      }

      const response = await apiClient.post<ApiResponse<TradeDepthAnalysis>>(
        '/api/v1/market/trade-depth',
        {
          region_filter: regionFilter && regionFilter !== 'all' ? regionFilter : undefined,
          date_range: dateRange,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
