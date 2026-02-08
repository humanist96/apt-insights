import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, BargainSalesAnalysis } from '@/types/analysis';
import { mockBargainSales } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

interface BargainSalesParams {
  regionFilter?: string;
  thresholdPct?: number;
  minTransactionCount?: number;
  startDate?: string;
  endDate?: string;
}

export function useBargainSales(params?: BargainSalesParams) {
  return useQuery<ApiResponse<BargainSalesAnalysis>>({
    queryKey: ['bargain-sales', params],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 500));

        const thresholdPct = params?.thresholdPct ?? 15;

        const filteredItems = mockBargainSales.data.bargain_items.filter((item) => {
          const regionMatch = !params?.regionFilter || params.regionFilter === 'all' || item.region === params.regionFilter;
          const discountMatch = item.discount_pct >= thresholdPct;
          return regionMatch && discountMatch;
        });

        const regionMap = new Map<string, { bargain: number; total: number }>();
        filteredItems.forEach((item) => {
          const current = regionMap.get(item.region) || { bargain: 0, total: 0 };
          current.bargain += 1;
          current.total += 1;
          regionMap.set(item.region, current);
        });

        const byRegion = Array.from(regionMap.entries()).map(([region, counts]) => ({
          region,
          bargain_count: counts.bargain,
          total_count: counts.total,
          bargain_rate: (counts.bargain / counts.total) * 100,
        })).sort((a, b) => b.bargain_rate - a.bargain_rate);

        const discounts = filteredItems.map(item => item.discount_pct);
        const totalSavings = filteredItems.reduce((sum, item) => sum + item.savings, 0);

        return {
          success: true,
          data: {
            bargain_items: filteredItems,
            stats: {
              total_trades: mockBargainSales.data.stats.total_trades,
              compared_trades: mockBargainSales.data.stats.compared_trades,
              bargain_count: filteredItems.length,
              bargain_rate: mockBargainSales.data.stats.compared_trades > 0
                ? (filteredItems.length / mockBargainSales.data.stats.compared_trades) * 100
                : 0,
              avg_discount: discounts.length > 0
                ? discounts.reduce((a, b) => a + b, 0) / discounts.length
                : 0,
              max_discount: discounts.length > 0 ? Math.max(...discounts) : 0,
              total_savings: totalSavings,
              threshold_pct: thresholdPct,
            },
            by_region: byRegion,
          },
        };
      }

      const response = await apiClient.post<ApiResponse<BargainSalesAnalysis>>(
        '/api/v1/investment/bargain-sales',
        {
          region_filter: params?.regionFilter && params.regionFilter !== 'all'
            ? params.regionFilter
            : undefined,
          threshold_pct: params?.thresholdPct,
          min_transaction_count: params?.minTransactionCount,
          start_date: params?.startDate,
          end_date: params?.endDate,
        }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
