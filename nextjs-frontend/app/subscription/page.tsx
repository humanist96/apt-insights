'use client';

import React, { useState } from 'react';
import { useSubscription } from '@/contexts/SubscriptionContext';
import PremiumBadge from '@/components/premium/PremiumBadge';
import Card from '@/components/ui/Card';

export default function SubscriptionPage() {
  const { subscription, plans, isPremium, isLoading, upgrade, cancel } = useSubscription();
  const [upgrading, setUpgrading] = useState(false);
  const [cancelling, setCancelling] = useState(false);

  const handleUpgrade = async (planId: string) => {
    if (upgrading) {
      return;
    }

    setUpgrading(true);
    try {
      const result = await upgrade(planId);
      if (result.success) {
        alert(result.message);
      } else {
        alert(`업그레이드 실패: ${result.message}`);
      }
    } finally {
      setUpgrading(false);
    }
  };

  const handleCancel = async () => {
    if (!confirm('정말 구독을 취소하시겠습니까?')) {
      return;
    }

    setCancelling(true);
    try {
      const result = await cancel();
      if (result.success) {
        alert(result.message);
      } else {
        alert(`취소 실패: ${result.message}`);
      }
    } finally {
      setCancelling(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
        </div>
      </div>
    );
  }

  const freePlan = plans.find((p) => p.tier === 'free');
  const premiumPlan = plans.find((p) => p.tier === 'premium');

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-2 text-3xl font-bold text-gray-900">구독 관리</h1>
      <p className="mb-8 text-gray-600">
        현재 플랜을 확인하고 프리미엄으로 업그레이드하세요
      </p>

      {subscription && (
        <Card className="mb-8">
          <h2 className="mb-4 text-xl font-bold text-gray-900">현재 구독</h2>
          <div className="mb-4 flex items-center gap-3">
            <span className="text-2xl font-bold text-gray-900">
              {subscription.plan_name}
            </span>
            {isPremium && <PremiumBadge size="md" />}
          </div>

          <div className="mb-4">
            <h3 className="mb-2 font-semibold text-gray-900">API 사용량</h3>
            <div className="rounded-lg bg-gray-50 p-4">
              {subscription.usage.unlimited ? (
                <div className="flex items-center gap-2">
                  <span className="text-2xl font-bold text-green-600">
                    무제한
                  </span>
                  <svg
                    className="h-6 w-6 text-green-500"
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
                </div>
              ) : (
                <>
                  <div className="mb-2 flex items-center justify-between">
                    <span className="text-sm text-gray-600">
                      오늘 사용량
                    </span>
                    <span className="font-semibold text-gray-900">
                      {subscription.usage.used} / {subscription.usage.limit}
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
                    <div
                      className={`h-full transition-all ${
                        subscription.usage.percentage >= 80
                          ? 'bg-red-500'
                          : subscription.usage.percentage >= 50
                          ? 'bg-yellow-500'
                          : 'bg-green-500'
                      }`}
                      style={{
                        width: `${Math.min(subscription.usage.percentage, 100)}%`,
                      }}
                    />
                  </div>
                  <p className="mt-2 text-xs text-gray-500">
                    매일 자정에 초기화됩니다
                  </p>
                </>
              )}
            </div>
          </div>

          {isPremium && subscription.expires_at && (
            <div className="mb-4">
              <p className="text-sm text-gray-600">
                만료일: {new Date(subscription.expires_at).toLocaleDateString('ko-KR')}
              </p>
            </div>
          )}

          {isPremium && (
            <button
              onClick={handleCancel}
              disabled={cancelling}
              className="rounded-lg border border-red-300 px-4 py-2 text-sm font-medium text-red-600 transition-colors hover:bg-red-50 disabled:opacity-50"
            >
              {cancelling ? '취소 중...' : '구독 취소'}
            </button>
          )}
        </Card>
      )}

      <h2 className="mb-6 text-2xl font-bold text-gray-900">구독 플랜</h2>

      <div className="grid gap-6 md:grid-cols-2">
        {freePlan && (
          <Card className={`${!isPremium ? 'ring-2 ring-blue-500' : ''}`}>
            <div className="mb-4">
              <h3 className="mb-2 text-xl font-bold text-gray-900">
                {freePlan.name}
              </h3>
              <p className="text-gray-600">{freePlan.description}</p>
            </div>

            <div className="mb-6">
              <span className="text-3xl font-bold text-gray-900">무료</span>
            </div>

            <div className="mb-6 space-y-3">
              <div className="flex items-start">
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
                <span className="text-sm text-gray-700">
                  하루 {freePlan.features.api_calls_per_day}회 API 호출
                </span>
              </div>
              <div className="flex items-start">
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
                <span className="text-sm text-gray-700">
                  기본 분석 기능
                </span>
              </div>
              <div className="flex items-start opacity-50">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400"
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
                <span className="text-sm text-gray-500">
                  CSV 내보내기
                </span>
              </div>
              <div className="flex items-start opacity-50">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400"
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
                <span className="text-sm text-gray-500">
                  PDF 리포트
                </span>
              </div>
              <div className="flex items-start opacity-50">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400"
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
                <span className="text-sm text-gray-500">
                  포트폴리오 추적
                </span>
              </div>
              <div className="flex items-start opacity-50">
                <svg
                  className="mr-2 mt-0.5 h-5 w-5 flex-shrink-0 text-gray-400"
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
                <span className="text-sm text-gray-500">
                  가격 알림
                </span>
              </div>
            </div>

            {!isPremium && (
              <div className="rounded-lg bg-blue-50 p-3 text-center text-sm text-blue-700">
                현재 플랜
              </div>
            )}
          </Card>
        )}

        {premiumPlan && (
          <Card
            className={`relative ${
              isPremium ? 'ring-2 ring-orange-500' : 'border-2 border-orange-200'
            }`}
          >
            {premiumPlan.popular && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <span className="rounded-full bg-orange-500 px-4 py-1 text-sm font-semibold text-white">
                  추천
                </span>
              </div>
            )}

            <div className="mb-4">
              <div className="mb-2 flex items-center gap-2">
                <h3 className="text-xl font-bold text-gray-900">
                  {premiumPlan.name}
                </h3>
                <PremiumBadge size="sm" />
              </div>
              <p className="text-gray-600">{premiumPlan.description}</p>
            </div>

            <div className="mb-6">
              <span className="text-3xl font-bold text-gray-900">
                {premiumPlan.price_monthly.toLocaleString()}원
              </span>
              <span className="text-gray-600">/월</span>
              {premiumPlan.price_yearly && (
                <p className="mt-1 text-sm text-gray-600">
                  연간 결제 시 {premiumPlan.price_yearly.toLocaleString()}원
                  (2개월 무료)
                </p>
              )}
            </div>

            <div className="mb-6 space-y-3">
              <div className="flex items-start">
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
                <span className="text-sm font-semibold text-gray-900">
                  무제한 API 호출
                </span>
              </div>
              <div className="flex items-start">
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
                <span className="text-sm text-gray-700">
                  기본 분석 기능
                </span>
              </div>
              <div className="flex items-start">
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
                <span className="text-sm font-semibold text-gray-900">
                  CSV 데이터 내보내기
                </span>
              </div>
              <div className="flex items-start">
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
                <span className="text-sm font-semibold text-gray-900">
                  PDF 리포트 생성
                </span>
              </div>
              <div className="flex items-start">
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
                <span className="text-sm font-semibold text-gray-900">
                  포트폴리오 추적 (최대 {premiumPlan.features.max_portfolios}개)
                </span>
              </div>
              <div className="flex items-start">
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
                <span className="text-sm font-semibold text-gray-900">
                  가격 알림 설정 (최대 {premiumPlan.features.max_alerts}개)
                </span>
              </div>
            </div>

            {isPremium ? (
              <div className="rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 p-3 text-center text-sm font-semibold text-white">
                현재 플랜
              </div>
            ) : (
              <button
                onClick={() => handleUpgrade(premiumPlan.plan_id)}
                disabled={upgrading}
                className="w-full rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-3 font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
              >
                {upgrading ? '업그레이드 중...' : '프리미엄 시작하기'}
              </button>
            )}
          </Card>
        )}
      </div>

      <div className="mt-8 rounded-lg bg-gray-50 p-6">
        <h3 className="mb-4 font-semibold text-gray-900">자주 묻는 질문</h3>
        <div className="space-y-4">
          <div>
            <p className="font-medium text-gray-900">
              언제든지 구독을 취소할 수 있나요?
            </p>
            <p className="mt-1 text-sm text-gray-600">
              네, 언제든지 구독을 취소할 수 있습니다. 구독 기간이 끝나면 자동으로 무료 플랜으로 전환됩니다.
            </p>
          </div>
          <div>
            <p className="font-medium text-gray-900">
              결제는 어떻게 진행되나요?
            </p>
            <p className="mt-1 text-sm text-gray-600">
              현재는 데모 버전으로 실제 결제가 진행되지 않습니다. 프리미엄 기능을 체험하실 수 있습니다.
            </p>
          </div>
          <div>
            <p className="font-medium text-gray-900">
              API 사용량은 언제 초기화되나요?
            </p>
            <p className="mt-1 text-sm text-gray-600">
              무료 플랜의 API 사용량은 매일 자정(KST)에 자동으로 초기화됩니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
