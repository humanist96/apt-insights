"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useSubscription } from "@/contexts/SubscriptionContext";
import { Crown, Check, X, Calendar, BarChart3, AlertCircle, Sparkles, TrendingUp, ChevronDown, ChevronUp, Zap } from "lucide-react";

export default function SubscriptionPage() {
  const { subscription, plans, isPremium, isLoading, upgrade, cancel } = useSubscription();
  const [upgrading, setUpgrading] = useState(false);
  const [cancelling, setCancelling] = useState(false);
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  const handleUpgrade = async (planId: string) => {
    if (upgrading) return;
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
    if (!confirm("정말 구독을 취소하시겠습니까?")) return;
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
      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-amber-500 to-orange-600 opacity-10 blur-3xl"
            animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>

        <div className="container relative mx-auto px-4 py-16">
          <div className="mb-12">
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-4xl font-bold text-transparent"
            >
              구독 관리
            </motion.h1>
            <p className="text-lg text-slate-400">프리미엄 플랜으로 더 많은 기능을 이용하세요</p>
          </div>

          <div className="space-y-8">
            <div className="h-64 w-full animate-pulse rounded-3xl bg-white/5"></div>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="h-96 animate-pulse rounded-3xl bg-white/5"></div>
              <div className="h-96 animate-pulse rounded-3xl bg-white/5"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const freePlan = plans.find((p) => p.tier === "free");
  const premiumPlan = plans.find((p) => p.tier === "premium");

  const usagePercentage = subscription?.usage?.unlimited
    ? 0
    : ((subscription?.usage?.used || 0) / (subscription?.usage?.limit || 10)) * 100;

  const faqs = [
    {
      question: "프리미엄 플랜의 혜택은 무엇인가요?",
      answer:
        "무제한 API 호출, CSV/PDF 내보내기, 포트폴리오 관리, 가격 알림, 월간 자동 리포트, AI 인사이트 등 모든 프리미엄 기능을 이용할 수 있습니다.",
    },
    {
      question: "언제든지 해지할 수 있나요?",
      answer: "네, 언제든지 구독을 해지할 수 있습니다. 해지 시 구독 기간이 끝나면 자동으로 무료 플랜으로 전환됩니다.",
    },
    {
      question: "무료 플랜으로 다운그레이드할 수 있나요?",
      answer:
        "네, 구독을 취소하면 만료일까지 프리미엄 혜택을 이용할 수 있으며, 만료 후 자동으로 무료 플랜으로 전환됩니다.",
    },
    {
      question: "결제는 어떻게 진행되나요?",
      answer: "현재는 데모 버전으로 실제 결제가 진행되지 않습니다. 프리미엄 기능을 체험하실 수 있습니다.",
    },
    {
      question: "API 사용량은 언제 초기화되나요?",
      answer: "무료 플랜의 API 사용량은 매일 자정(KST)에 자동으로 초기화됩니다.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-600/20 via-orange-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/4 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-amber-500 to-orange-600 opacity-10 blur-3xl"
          animate={{
            y: [0, 50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute right-1/3 top-40 h-80 w-80 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
          animate={{
            y: [0, -30, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="container relative mx-auto px-4 py-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/10 px-4 py-2">
            <Crown className="h-4 w-4 text-amber-400" />
            <span className="text-sm font-semibold text-amber-300">구독 관리</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-white via-amber-100 to-orange-200 bg-clip-text text-5xl font-bold text-transparent">
            구독 관리
          </h1>
          <p className="text-xl text-slate-400">프리미엄 플랜으로 더 많은 기능을 이용하세요</p>
        </motion.div>

        {/* Current Subscription Card */}
        {subscription && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-12 overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"
          >
            <div className="border-b border-white/10 p-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="mb-2 text-2xl font-bold text-white">현재 구독</h2>
                  <div className="flex items-center gap-3">
                    <span
                      className={`inline-flex items-center gap-2 rounded-full border px-4 py-2 ${
                        isPremium
                          ? "border-amber-500/20 bg-amber-500/10"
                          : "border-white/10 bg-white/5"
                      }`}
                    >
                      {isPremium && <Crown className="h-4 w-4 text-amber-400" />}
                      <span
                        className={`font-semibold ${
                          isPremium
                            ? "bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent"
                            : "text-slate-300"
                        }`}
                      >
                        {subscription.plan_name}
                      </span>
                    </span>
                  </div>
                </div>
                {isPremium && subscription.expires_at && (
                  <div className="text-right">
                    <p className="mb-1 text-sm text-slate-400">만료일</p>
                    <div className="flex items-center gap-2 text-lg font-semibold text-white">
                      <Calendar className="h-5 w-5 text-amber-400" />
                      {new Date(subscription.expires_at).toLocaleDateString("ko-KR")}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Usage Stats */}
            <div className="p-8">
              <div className="mb-6">
                <div className="mb-2 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-blue-400" />
                    <span className="font-medium text-white">API 사용량</span>
                  </div>
                  {subscription.usage?.unlimited ? (
                    <div className="flex items-center gap-2">
                      <Zap className="h-5 w-5 text-green-400" />
                      <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-sm font-semibold text-transparent">
                        무제한
                      </span>
                    </div>
                  ) : (
                    <span className="text-sm text-slate-400">
                      {subscription.usage?.used || 0} / {subscription.usage?.limit || 10}
                    </span>
                  )}
                </div>
                {!subscription.usage?.unlimited && (
                  <>
                    <div className="h-3 overflow-hidden rounded-full bg-white/5">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(usagePercentage, 100)}%` }}
                        transition={{ duration: 1, ease: "easeOut" }}
                        className={`h-full rounded-full ${
                          usagePercentage >= 90
                            ? "bg-gradient-to-r from-red-500 to-rose-500"
                            : usagePercentage >= 70
                              ? "bg-gradient-to-r from-amber-500 to-orange-500"
                              : "bg-gradient-to-r from-blue-500 to-cyan-500"
                        }`}
                      ></motion.div>
                    </div>
                    <p className="mt-2 text-xs text-slate-500">매일 자정에 초기화됩니다</p>
                  </>
                )}
              </div>

              {!isPremium && usagePercentage >= 70 && (
                <div className="mb-6 rounded-2xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-4">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="h-5 w-5 text-amber-400" />
                    <div>
                      <p className="mb-1 font-medium text-amber-300">API 사용량이 많습니다</p>
                      <p className="text-sm text-amber-400/80">
                        프리미엄으로 업그레이드하면 무제한으로 이용할 수 있습니다.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {isPremium && (
                <button
                  type="button"
                  onClick={handleCancel}
                  disabled={cancelling}
                  className="rounded-xl border border-red-500/30 bg-red-500/10 px-6 py-3 font-medium text-red-300 transition-all hover:border-red-500/50 hover:bg-red-500/20 disabled:opacity-50"
                >
                  {cancelling ? "취소 중..." : "구독 취소"}
                </button>
              )}
            </div>
          </motion.div>
        )}

        {/* Plan Comparison */}
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="mb-8 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-3xl font-bold text-transparent"
        >
          구독 플랜
        </motion.h2>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12 grid grid-cols-1 gap-6 lg:grid-cols-2"
        >
          {/* Free Plan */}
          {freePlan && (
            <div
              className={`group overflow-hidden rounded-3xl border bg-gradient-to-br from-white/5 to-white/0 p-8 backdrop-blur-sm ${
                !isPremium ? "border-blue-500/30" : "border-white/10"
              }`}
            >
              <div className="mb-6">
                <h3 className="mb-2 text-2xl font-bold text-white">{freePlan.name}</h3>
                <p className="text-slate-400">{freePlan.description}</p>
              </div>

              <div className="mb-8 flex items-baseline gap-2">
                <span className="text-4xl font-bold text-white">무료</span>
              </div>

              <ul className="mb-8 space-y-4">
                <li className="flex items-start gap-3">
                  <Check className="h-5 w-5 shrink-0 text-green-400" />
                  <span className="text-slate-300">
                    하루 {freePlan.features.api_calls_per_day}회 API 호출
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <Check className="h-5 w-5 shrink-0 text-green-400" />
                  <span className="text-slate-300">기본 분석 기능</span>
                </li>
                <li className="flex items-start gap-3 opacity-50">
                  <X className="h-5 w-5 shrink-0 text-red-400" />
                  <span className="text-slate-500">CSV 내보내기</span>
                </li>
                <li className="flex items-start gap-3 opacity-50">
                  <X className="h-5 w-5 shrink-0 text-red-400" />
                  <span className="text-slate-500">PDF 리포트</span>
                </li>
                <li className="flex items-start gap-3 opacity-50">
                  <X className="h-5 w-5 shrink-0 text-red-400" />
                  <span className="text-slate-500">포트폴리오 추적</span>
                </li>
                <li className="flex items-start gap-3 opacity-50">
                  <X className="h-5 w-5 shrink-0 text-red-400" />
                  <span className="text-slate-500">가격 알림</span>
                </li>
              </ul>

              {!isPremium ? (
                <div className="rounded-xl border border-blue-500/30 bg-blue-500/10 px-4 py-3 text-center font-medium text-blue-300">
                  현재 플랜
                </div>
              ) : (
                <button
                  type="button"
                  onClick={handleCancel}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 font-medium text-white transition-all hover:bg-white/10"
                >
                  다운그레이드
                </button>
              )}
            </div>
          )}

          {/* Premium Plan */}
          {premiumPlan && (
            <div
              className={`group relative overflow-hidden rounded-3xl border bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-8 backdrop-blur-sm ${
                isPremium ? "border-amber-500/30" : "border-amber-500/20"
              }`}
            >
              <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 to-orange-500 opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-20"></div>

              <div className="relative">
                {premiumPlan.popular && (
                  <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/20 px-3 py-1">
                    <Sparkles className="h-4 w-4 text-amber-400" />
                    <span className="text-sm font-semibold text-amber-300">인기</span>
                  </div>
                )}

                <div className="mb-6">
                  <div className="mb-2 flex items-center gap-2">
                    <h3 className="bg-gradient-to-r from-amber-200 to-orange-300 bg-clip-text text-2xl font-bold text-transparent">
                      {premiumPlan.name}
                    </h3>
                    <Crown className="h-6 w-6 text-amber-400" />
                  </div>
                  <p className="text-slate-400">{premiumPlan.description}</p>
                </div>

                <div className="mb-8 flex items-baseline gap-2">
                  <span className="bg-gradient-to-r from-amber-200 to-orange-300 bg-clip-text text-4xl font-bold text-transparent">
                    {premiumPlan.price_monthly.toLocaleString()}원
                  </span>
                  <span className="text-slate-400">/월</span>
                </div>
                {premiumPlan.price_yearly && (
                  <p className="mb-8 text-sm text-slate-400">
                    연간 결제 시 {premiumPlan.price_yearly.toLocaleString()}원 (2개월 무료)
                  </p>
                )}

                <ul className="mb-8 space-y-4">
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="font-semibold text-white">무제한 API 호출</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="text-white">모든 분석 기능</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="font-semibold text-white">CSV 데이터 내보내기</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="font-semibold text-white">PDF 리포트 생성</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="font-semibold text-white">
                      포트폴리오 추적 (최대 {premiumPlan.features.max_portfolios}개)
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="font-semibold text-white">
                      가격 알림 설정 (최대 {premiumPlan.features.max_alerts}개)
                    </span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="text-white">광고 제거</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <Check className="h-5 w-5 shrink-0 text-amber-400" />
                    <span className="text-white">우선 고객 지원</span>
                  </li>
                </ul>

                {isPremium ? (
                  <div className="rounded-xl border border-amber-500/30 bg-gradient-to-r from-amber-600 to-orange-600 px-4 py-3 text-center font-semibold text-white">
                    현재 플랜
                  </div>
                ) : (
                  <motion.button
                    type="button"
                    onClick={() => handleUpgrade(premiumPlan.plan_id)}
                    disabled={upgrading}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className="group relative w-full overflow-hidden rounded-xl disabled:opacity-50"
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-amber-600 to-orange-600"></div>
                    <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-orange-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
                    <div className="relative flex items-center justify-center gap-2 px-4 py-3 font-semibold text-white">
                      <TrendingUp className="h-5 w-5" />
                      {upgrading ? "업그레이드 중..." : "프리미엄 시작하기"}
                    </div>
                  </motion.button>
                )}
              </div>
            </div>
          )}
        </motion.div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-8 backdrop-blur-sm"
        >
          <h2 className="mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-2xl font-bold text-transparent">
            자주 묻는 질문
          </h2>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div
                key={index}
                className="overflow-hidden rounded-2xl border border-white/10 bg-white/5 transition-all hover:border-white/20"
              >
                <button
                  type="button"
                  onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
                  className="flex w-full items-center justify-between p-6 text-left transition-colors hover:bg-white/5"
                >
                  <span className="font-semibold text-white">{faq.question}</span>
                  {expandedFaq === index ? (
                    <ChevronUp className="h-5 w-5 shrink-0 text-slate-400" />
                  ) : (
                    <ChevronDown className="h-5 w-5 shrink-0 text-slate-400" />
                  )}
                </button>
                {expandedFaq === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-t border-white/10 px-6 py-4"
                  >
                    <p className="text-slate-300">{faq.answer}</p>
                  </motion.div>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
