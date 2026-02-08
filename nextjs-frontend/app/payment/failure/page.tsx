"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

function FailureContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const errorMessage = searchParams.get("error") || "결제 처리 중 오류가 발생했습니다.";

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg
              className="w-12 h-12 text-red-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">결제에 실패했습니다</h1>
          <p className="text-gray-600">{errorMessage}</p>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8 text-left">
          <h2 className="text-lg font-semibold text-yellow-900 mb-3">
            결제 실패 원인
          </h2>
          <ul className="text-sm text-yellow-800 space-y-2">
            <li>• 카드 정보가 올바르지 않을 수 있습니다</li>
            <li>• 결제 한도가 초과되었을 수 있습니다</li>
            <li>• 네트워크 연결이 불안정할 수 있습니다</li>
            <li>• 카드사에서 승인을 거부했을 수 있습니다</li>
          </ul>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 mb-8">
          <h3 className="font-semibold text-gray-900 mb-3">해결 방법</h3>
          <ol className="text-sm text-gray-700 space-y-2 text-left">
            <li>1. 카드 정보를 다시 확인하고 재시도해주세요</li>
            <li>2. 다른 카드로 결제를 시도해주세요</li>
            <li>3. 계좌이체 방식으로 결제해주세요</li>
            <li>4. 문제가 계속되면 고객지원에 문의해주세요</li>
          </ol>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/payment"
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
          >
            다시 시도
          </Link>
          <Link
            href="/"
            className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-semibold"
          >
            홈으로
          </Link>
        </div>

        <div className="mt-8 text-sm text-gray-500">
          <p>
            도움이 필요하신가요?{" "}
            <a href="mailto:support@example.com" className="text-blue-600 hover:underline">
              고객지원
            </a>
            으로 문의해주세요.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function PaymentFailurePage() {
  return (
    <Suspense
      fallback={
        <div className="container mx-auto px-4 py-8 max-w-2xl">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <p>로딩 중...</p>
          </div>
        </div>
      }
    >
      <FailureContent />
    </Suspense>
  );
}
