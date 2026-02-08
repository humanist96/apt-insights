"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  CreditCard,
  Banknote,
  Lock,
  CheckCircle2,
  AlertCircle,
  Shield,
  Sparkles,
} from "lucide-react";
import { apiClient } from "@/lib/api-client";

interface PaymentForm {
  cardNumber: string;
  expiryDate: string;
  cvv: string;
  agreeTerms: boolean;
}

const PLAN_PRICE = 9900;

export default function PaymentPage() {
  const router = useRouter();
  const [selectedMethod, setSelectedMethod] = useState<"card" | "bank_transfer">("card");
  const [form, setForm] = useState<PaymentForm>({
    cardNumber: "",
    expiryDate: "",
    cvv: "",
    agreeTerms: false,
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (field: keyof PaymentForm, value: string | boolean) => {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
    setError(null);
  };

  const formatCardNumber = (value: string): string => {
    const cleaned = value.replace(/\D/g, "");
    const limited = cleaned.slice(0, 16);
    return limited.replace(/(\d{4})(?=\d)/g, "$1 ");
  };

  const formatExpiryDate = (value: string): string => {
    const cleaned = value.replace(/\D/g, "");
    const limited = cleaned.slice(0, 4);
    if (limited.length >= 2) {
      return `${limited.slice(0, 2)}/${limited.slice(2)}`;
    }
    return limited;
  };

  const validateForm = (): boolean => {
    if (selectedMethod === "card") {
      const cardNumberClean = form.cardNumber.replace(/\s/g, "");
      if (cardNumberClean.length !== 16) {
        setError("카드번호 16자리를 입력해주세요");
        return false;
      }

      const expiryClean = form.expiryDate.replace(/\//g, "");
      if (expiryClean.length !== 4) {
        setError("유효기간을 MM/YY 형식으로 입력해주세요");
        return false;
      }

      if (form.cvv.length !== 3) {
        setError("CVV 3자리를 입력해주세요");
        return false;
      }
    }

    if (!form.agreeTerms) {
      setError("이용약관에 동의해주세요");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        router.push("/login?redirect=/payment");
        return;
      }

      const createResponse = await apiClient.post(
        "/api/v1/payments/create",
        {
          amount: PLAN_PRICE,
          currency: "KRW",
          payment_method: selectedMethod,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const { portone_payment_id } = createResponse.data;

      const verifyResponse = await apiClient.post(
        "/api/v1/payments/verify",
        {
          portone_payment_id,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (verifyResponse.data.success) {
        router.push(`/payment/success?receipt=${verifyResponse.data.receipt_number}`);
      } else {
        throw new Error("결제 검증에 실패했습니다");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "결제 처리 중 오류가 발생했습니다");
      setIsProcessing(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Animated background orbs */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -left-32 top-0 h-96 w-96 rounded-full bg-gradient-to-r from-amber-500/20 to-orange-500/20 blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, 50, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute -right-32 top-1/3 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500/20 to-pink-500/20 blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, -50, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto max-w-3xl px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12 text-center"
        >
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/10 px-4 py-2 backdrop-blur-sm">
            <Sparkles className="h-4 w-4 text-amber-400" />
            <span className="text-sm font-medium text-amber-300">프리미엄 구독</span>
          </div>
          <h1 className="mb-4 bg-gradient-to-r from-amber-200 via-orange-200 to-pink-200 bg-clip-text text-5xl font-bold text-transparent">
            프리미엄으로 업그레이드
          </h1>
          <p className="text-lg text-slate-400">
            무제한 데이터 조회와 프리미엄 기능을 이용하세요
          </p>
        </motion.div>

        {/* Plan Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8 overflow-hidden rounded-3xl border border-amber-500/30 bg-gradient-to-br from-amber-500/20 via-orange-500/10 to-pink-500/5 p-8 backdrop-blur-sm"
        >
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-amber-100">월간 프리미엄 플랜</h2>
              <p className="mt-1 text-sm text-amber-300/60">매월 자동 갱신</p>
            </div>
            <div className="text-right">
              <p className="text-4xl font-bold text-amber-100">
                ₩{PLAN_PRICE.toLocaleString()}
              </p>
              <p className="text-sm text-amber-300/60">/ 월</p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            {[
              "무제한 데이터 조회",
              "CSV/PDF 내보내기",
              "프리미엄 분석 기능",
              "우선 고객 지원",
            ].map((feature, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-amber-400" />
                <span className="text-sm text-amber-100/80">{feature}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Payment Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="overflow-hidden rounded-3xl border border-slate-700/50 bg-gradient-to-br from-slate-800/80 to-slate-900/80 p-8 backdrop-blur-sm"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Payment Method Selection */}
            <div>
              <label className="mb-3 block text-sm font-medium text-slate-300">
                결제 수단 선택
              </label>
              <div className="grid grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => setSelectedMethod("card")}
                  disabled={isProcessing}
                  className={`group relative overflow-hidden rounded-2xl border-2 p-6 transition-all ${
                    selectedMethod === "card"
                      ? "border-amber-500/50 bg-gradient-to-br from-amber-500/20 to-orange-500/10"
                      : "border-slate-600/50 bg-slate-800/30 hover:border-slate-500/50"
                  }`}
                >
                  <div className="relative flex flex-col items-center gap-2">
                    <CreditCard
                      className={`h-8 w-8 transition-colors ${
                        selectedMethod === "card" ? "text-amber-400" : "text-slate-400"
                      }`}
                    />
                    <span
                      className={`text-sm font-medium ${
                        selectedMethod === "card" ? "text-amber-100" : "text-slate-400"
                      }`}
                    >
                      신용/체크카드
                    </span>
                  </div>
                </button>

                <button
                  type="button"
                  onClick={() => setSelectedMethod("bank_transfer")}
                  disabled={isProcessing}
                  className={`group relative overflow-hidden rounded-2xl border-2 p-6 transition-all ${
                    selectedMethod === "bank_transfer"
                      ? "border-amber-500/50 bg-gradient-to-br from-amber-500/20 to-orange-500/10"
                      : "border-slate-600/50 bg-slate-800/30 hover:border-slate-500/50"
                  }`}
                >
                  <div className="relative flex flex-col items-center gap-2">
                    <Banknote
                      className={`h-8 w-8 transition-colors ${
                        selectedMethod === "bank_transfer" ? "text-amber-400" : "text-slate-400"
                      }`}
                    />
                    <span
                      className={`text-sm font-medium ${
                        selectedMethod === "bank_transfer" ? "text-amber-100" : "text-slate-400"
                      }`}
                    >
                      계좌이체
                    </span>
                  </div>
                </button>
              </div>
            </div>

            {/* Card Form */}
            {selectedMethod === "card" && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="space-y-4"
              >
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">
                    카드번호
                  </label>
                  <input
                    type="text"
                    value={form.cardNumber}
                    onChange={(e) =>
                      handleInputChange("cardNumber", formatCardNumber(e.target.value))
                    }
                    placeholder="1234 5678 9012 3456"
                    disabled={isProcessing}
                    className="w-full rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-3 text-slate-200 backdrop-blur-sm transition-all placeholder:text-slate-500 hover:border-amber-500/50 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                      유효기간
                    </label>
                    <input
                      type="text"
                      value={form.expiryDate}
                      onChange={(e) =>
                        handleInputChange("expiryDate", formatExpiryDate(e.target.value))
                      }
                      placeholder="MM/YY"
                      disabled={isProcessing}
                      className="w-full rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-3 text-slate-200 backdrop-blur-sm transition-all placeholder:text-slate-500 hover:border-amber-500/50 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                  </div>

                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                      CVV
                    </label>
                    <input
                      type="text"
                      value={form.cvv}
                      onChange={(e) =>
                        handleInputChange("cvv", e.target.value.replace(/\D/g, "").slice(0, 3))
                      }
                      placeholder="123"
                      disabled={isProcessing}
                      className="w-full rounded-xl border border-slate-600/50 bg-slate-800/50 px-4 py-3 text-slate-200 backdrop-blur-sm transition-all placeholder:text-slate-500 hover:border-amber-500/50 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                    />
                  </div>
                </div>
              </motion.div>
            )}

            {/* Bank Transfer Notice */}
            {selectedMethod === "bank_transfer" && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/5 p-6 backdrop-blur-sm"
              >
                <div className="flex items-start gap-3">
                  <Banknote className="h-5 w-5 text-blue-400" />
                  <p className="text-sm text-blue-400/80">
                    계좌이체 정보는 다음 단계에서 제공됩니다.
                  </p>
                </div>
              </motion.div>
            )}

            {/* Terms Checkbox */}
            <div>
              <label className="flex cursor-pointer items-start gap-3 rounded-xl border border-slate-600/50 bg-slate-800/30 p-4 transition-colors hover:border-slate-500/50">
                <input
                  type="checkbox"
                  checked={form.agreeTerms}
                  onChange={(e) => handleInputChange("agreeTerms", e.target.checked)}
                  disabled={isProcessing}
                  className="mt-1 h-5 w-5 cursor-pointer rounded border-slate-600 bg-slate-700 text-amber-500 focus:ring-2 focus:ring-amber-500/20 disabled:cursor-not-allowed"
                />
                <span className="flex-1 text-sm text-slate-300">
                  이용약관 및 개인정보 처리방침에 동의합니다. (필수)
                </span>
              </label>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="rounded-2xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-red-600/5 p-4 backdrop-blur-sm"
              >
                <div className="flex items-center gap-3">
                  <AlertCircle className="h-5 w-5 text-red-400" />
                  <p className="text-sm text-red-400">{error}</p>
                </div>
              </motion.div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isProcessing}
              className="group relative w-full overflow-hidden rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 px-8 py-4 font-semibold text-white shadow-lg transition-all hover:shadow-xl hover:shadow-amber-500/20 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-amber-400 to-orange-400 opacity-0 transition-opacity group-hover:opacity-100" />
              <span className="relative flex items-center justify-center gap-2">
                {isProcessing ? (
                  <>
                    <div className="h-5 w-5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                    결제 처리 중...
                  </>
                ) : (
                  <>
                    <Lock className="h-5 w-5" />₩{PLAN_PRICE.toLocaleString()} 결제하기
                  </>
                )}
              </span>
            </button>
          </form>
        </motion.div>

        {/* Security Notice */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-8 text-center"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/10 px-4 py-2 backdrop-blur-sm">
            <Shield className="h-4 w-4 text-green-400" />
            <span className="text-sm text-green-400">SSL 암호화로 안전하게 보호됩니다</span>
          </div>
          <p className="mt-4 text-sm text-slate-500">
            언제든지 구독을 취소할 수 있습니다.
          </p>
        </motion.div>
      </div>
    </div>
  );
}
