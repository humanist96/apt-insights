import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, JeonseRatioAnalysis } from '@/types/analysis';
import { mockJeonseRatio } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface JeonseAnalysisParams {
  regionFilter?: string;
  minJeonseRatio?: number;
  startDate?: string;
  endDate?: string;
}

export function useJeonseAnalysis(params?: JeonseAnalysisParams) {
  return useQuery<ApiResponse<JeonseRatioAnalysis>>({
    queryKey: ['jeonse-analysis', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));

        if (params?.regionFilter && params.regionFilter !== 'all') {
          const filteredRegions = mockJeonseRatio.data.by_region.filter(
            (item) => item.region === params.regionFilter
          );

          return {
            ...mockJeonseRatio,
            data: {
              ...mockJeonseRatio.data,
              by_region: filteredRegions,
            },
          };
        }

        return mockJeonseRatio;
      }

      const response = await apiClient.post<ApiResponse<JeonseRatioAnalysis>>(
        '/api/v1/investment/jeonse-ratio',
        {
          region_filter: params?.regionFilter && params.regionFilter !== 'all'
            ? params.regionFilter
            : undefined,
          min_jeonse_ratio: params?.minJeonseRatio,
          start_date: params?.startDate,
          end_date: params?.endDate,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
