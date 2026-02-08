import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, RentVsJeonseAnalysis } from '@/types/analysis';
import { mockRentVsJeonse } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface RentVsJeonseParams {
  regionFilter?: string;
  startDate?: string;
  endDate?: string;
}

export function useRentVsJeonse(params?: RentVsJeonseParams) {
  return useQuery<ApiResponse<RentVsJeonseAnalysis>>({
    queryKey: ['rent-vs-jeonse', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));

        if (params?.regionFilter && params.regionFilter !== 'all') {
          const filteredRegions = mockRentVsJeonse.data.by_region.filter(
            (item) => item.region === params.regionFilter
          );

          if (filteredRegions.length > 0) {
            const regionData = filteredRegions[0];
            return {
              ...mockRentVsJeonse,
              data: {
                ...mockRentVsJeonse.data,
                by_region: filteredRegions,
                stats: {
                  ...mockRentVsJeonse.data.stats,
                  total_count: regionData.total_count,
                  jeonse_count: regionData.jeonse_count,
                  wolse_count: regionData.wolse_count,
                  jeonse_ratio: regionData.jeonse_ratio,
                  wolse_ratio: regionData.wolse_ratio,
                },
              },
            };
          }
        }

        return mockRentVsJeonse;
      }

      const response = await apiClient.post<ApiResponse<RentVsJeonseAnalysis>>(
        '/api/v1/market/rent-vs-jeonse',
        {
          region_filter: params?.regionFilter && params.regionFilter !== 'all'
            ? params.regionFilter
            : undefined,
          start_date: params?.startDate,
          end_date: params?.endDate,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
