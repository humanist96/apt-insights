import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { ApiResponse, DetailDataResponse, DetailDataFilters, DetailDataItem } from '@/types/analysis';
import { mockDetailData } from '@/lib/mock-data';

const USE_MOCK_DATA = true;

export function useDetailData(filters: DetailDataFilters, page: number = 1, pageSize: number = 50) {
  const { data, isLoading, error } = useQuery<ApiResponse<DetailDataResponse>>({
    queryKey: ['detail-data', filters, page, pageSize],
    queryFn: async () => {
      if (USE_MOCK_DATA) {
        await new Promise((resolve) => setTimeout(resolve, 300));
        return mockDetailData;
      }

      const response = await apiClient.post<ApiResponse<DetailDataResponse>>(
        '/api/v1/analysis/detail-data',
        { filters, page, page_size: pageSize }
      );
      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });

  const filteredData = useMemo(() => {
    if (!data?.success || !data?.data?.items) {
      return { items: [], total: 0 };
    }

    let items = data.data.items;

    if (filters.regions.length > 0) {
      items = items.filter((item) => filters.regions.includes(item.region));
    }

    if (filters.dateStart) {
      items = items.filter((item) => item.deal_date >= filters.dateStart!);
    }

    if (filters.dateEnd) {
      items = items.filter((item) => item.deal_date <= filters.dateEnd!);
    }

    if (filters.priceMin !== undefined && filters.priceMin > 0) {
      items = items.filter((item) => item.deal_amount >= filters.priceMin!);
    }

    if (filters.priceMax !== undefined && filters.priceMax > 0) {
      items = items.filter((item) => item.deal_amount <= filters.priceMax!);
    }

    if (filters.areaMin !== undefined && filters.areaMin > 0) {
      items = items.filter((item) => item.area >= filters.areaMin!);
    }

    if (filters.areaMax !== undefined && filters.areaMax > 0) {
      items = items.filter((item) => item.area <= filters.areaMax!);
    }

    if (filters.floorMin !== undefined && filters.floorMin > 0) {
      items = items.filter((item) => item.floor >= filters.floorMin!);
    }

    if (filters.floorMax !== undefined && filters.floorMax > 0) {
      items = items.filter((item) => item.floor <= filters.floorMax!);
    }

    if (filters.transactionTypes.length > 0) {
      items = items.filter((item) => filters.transactionTypes.includes(item.transaction_type));
    }

    if (filters.searchQuery && filters.searchQuery.trim()) {
      const query = filters.searchQuery.trim().toLowerCase();
      items = items.filter((item) =>
        item.apt_name.toLowerCase().includes(query) ||
        item.region.toLowerCase().includes(query)
      );
    }

    return { items, total: items.length };
  }, [data, filters]);

  const paginatedData = useMemo(() => {
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return filteredData.items.slice(startIndex, endIndex);
  }, [filteredData.items, page, pageSize]);

  return {
    data: paginatedData,
    totalCount: filteredData.total,
    totalPages: Math.ceil(filteredData.total / pageSize),
    isLoading,
    error,
  };
}
