'use client';

import React, { useState } from 'react';
import { useSubscription } from '@/contexts/SubscriptionContext';
import { subscriptionApi } from '@/lib/api/subscriptions';
import PremiumFeatureGate from '@/components/premium/PremiumFeatureGate';

interface ExportButtonsProps {
  data?: any;
  filters?: Record<string, any>;
  className?: string;
}

export default function ExportButtons({ data, filters, className = '' }: ExportButtonsProps) {
  const { checkFeatureAccess } = useSubscription();
  const [exporting, setExporting] = useState(false);

  const handleCsvExport = async () => {
    if (!checkFeatureAccess('csv_export')) {
      return;
    }

    setExporting(true);
    try {
      const blob = await subscriptionApi.exportCsv({
        export_type: 'csv',
        filters,
      });

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `apartment_data_${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error: any) {
      if (error.response?.status === 403) {
        alert('CSV 내보내기는 프리미엄 기능입니다');
      } else {
        alert('CSV 내보내기 실패');
      }
    } finally {
      setExporting(false);
    }
  };

  const handlePdfExport = async () => {
    if (!checkFeatureAccess('pdf_export')) {
      return;
    }

    setExporting(true);
    try {
      const result = await subscriptionApi.exportPdf({
        export_type: 'pdf',
        filters,
      });

      if (result.success) {
        alert(result.message || 'PDF 생성이 시작되었습니다');
      }
    } catch (error: any) {
      if (error.response?.status === 403) {
        alert('PDF 내보내기는 프리미엄 기능입니다');
      } else {
        alert('PDF 내보내기 실패');
      }
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className={`flex gap-3 ${className}`}>
      <PremiumFeatureGate
        feature="csv_export"
        featureName="CSV 데이터 내보내기"
        fallback={
          <button
            className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
            disabled={exporting}
          >
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>CSV 내보내기</span>
            <span className="ml-1 rounded bg-orange-100 px-1.5 py-0.5 text-xs text-orange-600">
              Premium
            </span>
          </button>
        }
      >
        <button
          onClick={handleCsvExport}
          disabled={exporting}
          className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 disabled:opacity-50"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <span>{exporting ? '내보내는 중...' : 'CSV 내보내기'}</span>
        </button>
      </PremiumFeatureGate>

      <PremiumFeatureGate
        feature="pdf_export"
        featureName="PDF 리포트 생성"
        fallback={
          <button
            className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
            disabled={exporting}
          >
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>PDF 내보내기</span>
            <span className="ml-1 rounded bg-orange-100 px-1.5 py-0.5 text-xs text-orange-600">
              Premium
            </span>
          </button>
        }
      >
        <button
          onClick={handlePdfExport}
          disabled={exporting}
          className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 disabled:opacity-50"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <span>{exporting ? '생성 중...' : 'PDF 내보내기'}</span>
        </button>
      </PremiumFeatureGate>
    </div>
  );
}
