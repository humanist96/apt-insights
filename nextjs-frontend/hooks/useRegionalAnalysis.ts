import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, RegionalAnalysis } from '@/types/analysis';
import { mockRegionalData, mockRegionalDataFiltered } from '@/lib/mock-data';

const USE_MOCK_DATA = true; // Set to false when backend is ready

export function useRegionalAnalysis(regionFilter?: string) {
  return useQuery<ApiResponse<RegionalAnalysis>>({
    queryKey: ['regional-analysis', regionFilter],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 500));

        if (regionFilter && regionFilter !== 'all') {
          return mockRegionalDataFiltered(regionFilter);
        }
        return mockRegionalData;
      }

      const response = await apiClient.post<ApiResponse<RegionalAnalysis>>(
        '/api/v1/analysis/regional',
        {
          region_filter: regionFilter && regionFilter !== 'all' ? regionFilter : undefined,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
