import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, ApartmentAnalysis } from '@/types/analysis';
import { mockByApartment } from '@/lib/mock-data';

const USE_MOCK_DATA = true; // Set to false when backend is ready

interface ApartmentFilters {
  region?: string;
  minCount?: number;
  search?: string;
}

export function useByApartment(filters?: ApartmentFilters) {
  return useQuery<ApiResponse<ApartmentAnalysis>>({
    queryKey: ['apartment-analysis', filters],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));

        let filteredData = [...mockByApartment.data.data];

        if (filters?.region && filters.region !== 'all') {
          filteredData = filteredData.filter((apt) => apt.region === filters.region);
        }

        if (filters?.minCount !== undefined) {
          filteredData = filteredData.filter(
            (apt) => apt.count >= (filters.minCount ?? 0)
          );
        }

        if (filters?.search) {
          const searchLower = filters.search.toLowerCase();
          filteredData = filteredData.filter((apt) =>
            apt.apt_name.toLowerCase().includes(searchLower)
          );
        }

        return {
          success: true,
          data: {
            data: filteredData,
          },
        };
      }

      const response = await apiClient.post<ApiResponse<ApartmentAnalysis>>(
        '/api/v1/analysis/by-apartment',
        {
          region_filter: filters?.region && filters.region !== 'all' ? filters.region : undefined,
          min_count: filters?.minCount,
          search_term: filters?.search,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
