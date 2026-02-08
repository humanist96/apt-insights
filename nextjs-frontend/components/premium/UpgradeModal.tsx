'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import PremiumBadge from './PremiumBadge';

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  featureName?: string;
}

export default function UpgradeModal({
  isOpen,
  onClose,
  featureName = '이 기능',
}: UpgradeModalProps) {
  const router = useRouter();

  if (!isOpen) {
    return null;
  }

  const handleUpgrade = () => {
    onClose();
    router.push('/subscription');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">프리미엄 기능</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            aria-label="닫기"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <div className="mb-6">
          <div className="mb-4 flex items-center gap-2">
            <PremiumBadge size="md" />
            <span className="text-sm text-gray-600">전용 기능</span>
          </div>

          <p className="mb-4 text-gray-700">
            <strong>{featureName}</strong>는 프리미엄 플랜에서 이용 가능합니다.
          </p>

          <div className="rounded-lg bg-gradient-to-br from-amber-50 to-orange-50 p-4">
            <h3 className="mb-2 font-semibold text-gray-900">프리미엄 혜택</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-green-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span>무제한 API 호출</span>
              </li>
              <li className="flex items-start">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-green-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span>CSV 데이터 내보내기</span>
              </li>
              <li className="flex items-start">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-green-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span>PDF 리포트 생성</span>
              </li>
              <li className="flex items-start">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-green-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span>포트폴리오 추적 (최대 50개)</span>
              </li>
              <li className="flex items-start">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-green-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span>가격 알림 설정 (최대 10개)</span>
              </li>
            </ul>
          </div>

          <div className="mt-4 text-center">
            <p className="text-2xl font-bold text-gray-900">
              월 9,900원
            </p>
            <p className="text-sm text-gray-600">
              연간 결제 시 99,000원 (2개월 무료)
            </p>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2.5 font-medium text-gray-700 transition-colors hover:bg-gray-50"
          >
            나중에
          </button>
          <button
            onClick={handleUpgrade}
            className="flex-1 rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-2.5 font-medium text-white transition-opacity hover:opacity-90"
          >
            업그레이드
          </button>
        </div>
      </div>
    </div>
  );
}
