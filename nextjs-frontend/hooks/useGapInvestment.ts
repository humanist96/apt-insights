import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, GapInvestmentAnalysis } from '@/types/analysis';
import { mockGapInvestment } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface GapInvestmentParams {
  regionFilter?: string;
  minGapRatio?: number;
  maxGap?: number;
  startDate?: string;
  endDate?: string;
}

export function useGapInvestment(params?: GapInvestmentParams) {
  return useQuery<ApiResponse<GapInvestmentAnalysis>>({
    queryKey: ['gap-investment', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));

        if (params?.regionFilter && params.regionFilter !== 'all') {
          const filteredOpportunities = mockGapInvestment.data.opportunities.filter(
            (item) => item.region === params.regionFilter
          );

          return {
            ...mockGapInvestment,
            data: {
              ...mockGapInvestment.data,
              opportunities: filteredOpportunities,
              gap_stats: {
                ...mockGapInvestment.data.gap_stats,
                total_count: filteredOpportunities.length,
              },
            },
          };
        }

        return mockGapInvestment;
      }

      const response = await apiClient.post<ApiResponse<GapInvestmentAnalysis>>(
        '/api/v1/investment/gap-investment',
        {
          region_filter: params?.regionFilter && params.regionFilter !== 'all'
            ? params.regionFilter
            : undefined,
          min_gap_ratio: params?.minGapRatio,
          max_gap: params?.maxGap,
          start_date: params?.startDate,
          end_date: params?.endDate,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
