"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

function SuccessContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [receiptNumber, setReceiptNumber] = useState<string | null>(null);

  useEffect(() => {
    const receipt = searchParams.get("receipt");
    setReceiptNumber(receipt);

    if (!receipt) {
      router.push("/");
    }
  }, [searchParams, router]);

  if (!receiptNumber) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg
              className="w-12 h-12 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">결제가 완료되었습니다!</h1>
          <p className="text-gray-600">프리미엄 구독이 활성화되었습니다.</p>
        </div>

        <div className="bg-gray-50 rounded-lg p-6 mb-8 text-left">
          <h2 className="text-lg font-semibold mb-4">결제 정보</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">영수증 번호</span>
              <span className="font-mono">{receiptNumber}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">구독 플랜</span>
              <span>월간 프리미엄</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">결제 금액</span>
              <span className="font-semibold">₩9,900</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">다음 결제일</span>
              <span>
                {new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toLocaleDateString(
                  "ko-KR"
                )}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <h3 className="font-semibold text-blue-900 mb-2">프리미엄 혜택</h3>
          <ul className="text-sm text-blue-800 space-y-1 text-left">
            <li>• 무제한 데이터 조회 및 분석</li>
            <li>• CSV/PDF 내보내기 기능</li>
            <li>• 프리미엄 분석 도구 사용</li>
            <li>• 우선 고객 지원</li>
          </ul>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/"
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
          >
            시작하기
          </Link>
          <Link
            href="/profile"
            className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-semibold"
          >
            구독 관리
          </Link>
        </div>

        <div className="mt-8 text-sm text-gray-500">
          <p>영수증은 이메일로 발송되었습니다.</p>
          <p className="mt-1">
            문의사항이 있으시면{" "}
            <a href="mailto:support@example.com" className="text-blue-600 hover:underline">
              고객지원
            </a>
            으로 연락주세요.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function PaymentSuccessPage() {
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
      <SuccessContent />
    </Suspense>
  );
}
