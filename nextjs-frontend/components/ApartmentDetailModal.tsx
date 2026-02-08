'use client';

import { ApartmentDataItem } from '@/types/analysis';
import { X } from 'lucide-react';

interface ApartmentDetailModalProps {
  apartment: ApartmentDataItem | null;
  isOpen: boolean;
  onClose: () => void;
}

export default function ApartmentDetailModal({
  apartment,
  isOpen,
  onClose,
}: ApartmentDetailModalProps) {
  if (!isOpen || !apartment) return null;

  const formatPrice = (price?: number) => {
    if (!price) return '-';
    return `${(price / 10000).toLocaleString('ko-KR', { maximumFractionDigits: 0 })}억원`;
  };

  const formatPricePerArea = (price?: number) => {
    if (!price) return '-';
    return `${price.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}만원/㎡`;
  };

  const formatArea = (area?: number) => {
    if (!area) return '-';
    return `${area.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}㎡`;
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                {apartment.apt_name}
              </h2>
              {apartment.region && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {apartment.region}
                </p>
              )}
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              aria-label="닫기"
            >
              <X className="w-6 h-6 text-gray-600 dark:text-gray-400" />
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-6 space-y-6">
            {/* Overview Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                <p className="text-sm text-blue-600 dark:text-blue-400 mb-1">총 거래건수</p>
                <p className="text-2xl font-bold text-blue-900 dark:text-blue-300">
                  {apartment.count.toLocaleString('ko-KR')}건
                </p>
              </div>
              <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
                <p className="text-sm text-green-600 dark:text-green-400 mb-1">평균 가격</p>
                <p className="text-2xl font-bold text-green-900 dark:text-green-300">
                  {formatPrice(apartment.avg_price)}
                </p>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
                <p className="text-sm text-purple-600 dark:text-purple-400 mb-1">평당가</p>
                <p className="text-2xl font-bold text-purple-900 dark:text-purple-300">
                  {formatPricePerArea(apartment.avg_price_per_area)}
                </p>
              </div>
              <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
                <p className="text-sm text-orange-600 dark:text-orange-400 mb-1">건축년도</p>
                <p className="text-2xl font-bold text-orange-900 dark:text-orange-300">
                  {apartment.build_year || 'N/A'}
                </p>
              </div>
            </div>

            {/* Price Range */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-3">가격 범위</h3>
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">최고가</p>
                  <p className="text-lg font-bold text-gray-900 dark:text-white">
                    {formatPrice(apartment.max_price)}
                  </p>
                </div>
                <div className="hidden md:block text-2xl text-gray-400">~</div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">최저가</p>
                  <p className="text-lg font-bold text-gray-900 dark:text-white">
                    {formatPrice(apartment.min_price)}
                  </p>
                </div>
              </div>
              {apartment.floor_range && (
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400">층수 범위</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-white">
                    {apartment.floor_range}층
                  </p>
                </div>
              )}
            </div>

            {/* Recent Deals */}
            {apartment.deals && apartment.deals.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
                  최근 거래 내역 ({apartment.deals.length}건)
                </h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-700 dark:text-gray-300 uppercase">
                          거래일
                        </th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase">
                          가격
                        </th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase">
                          면적
                        </th>
                        <th className="px-4 py-2 text-center text-xs font-medium text-gray-700 dark:text-gray-300 uppercase">
                          층
                        </th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-700 dark:text-gray-300 uppercase">
                          평당가
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                      {apartment.deals.map((deal, index) => (
                        <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                          <td className="px-4 py-2 text-sm text-gray-900 dark:text-white">
                            {deal.deal_date}
                          </td>
                          <td className="px-4 py-2 text-sm text-right text-gray-900 dark:text-white">
                            {formatPrice(deal.price)}
                          </td>
                          <td className="px-4 py-2 text-sm text-right text-gray-600 dark:text-gray-400">
                            {formatArea(deal.area)}
                          </td>
                          <td className="px-4 py-2 text-sm text-center text-gray-600 dark:text-gray-400">
                            {deal.floor}
                          </td>
                          <td className="px-4 py-2 text-sm text-right text-gray-900 dark:text-white">
                            {formatPricePerArea(deal.price_per_area)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {(!apartment.deals || apartment.deals.length === 0) && (
              <div className="text-center py-8">
                <p className="text-gray-600 dark:text-gray-400">
                  거래 내역 정보가 없습니다
                </p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 px-6 py-4">
            <button
              onClick={onClose}
              className="w-full px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
            >
              닫기
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
