"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
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
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-6">프리미엄 구독</h1>

        <div className="mb-8 p-6 bg-blue-50 rounded-lg">
          <div className="flex justify-between items-center mb-2">
            <span className="text-lg font-semibold">월간 프리미엄 플랜</span>
            <span className="text-2xl font-bold text-blue-600">₩{PLAN_PRICE.toLocaleString()}</span>
          </div>
          <ul className="text-sm text-gray-600 space-y-1 mt-4">
            <li>• 무제한 데이터 조회</li>
            <li>• CSV/PDF 내보내기</li>
            <li>• 프리미엄 분석 기능</li>
            <li>• 우선 고객 지원</li>
          </ul>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              결제 수단
            </label>
            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => setSelectedMethod("card")}
                className={`p-4 border-2 rounded-lg ${
                  selectedMethod === "card"
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200"
                }`}
              >
                신용/체크카드
              </button>
              <button
                type="button"
                onClick={() => setSelectedMethod("bank_transfer")}
                className={`p-4 border-2 rounded-lg ${
                  selectedMethod === "bank_transfer"
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200"
                }`}
              >
                계좌이체
              </button>
            </div>
          </div>

          {selectedMethod === "card" && (
            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  카드번호
                </label>
                <input
                  type="text"
                  value={form.cardNumber}
                  onChange={(e) =>
                    handleInputChange("cardNumber", formatCardNumber(e.target.value))
                  }
                  placeholder="1234 5678 9012 3456"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  disabled={isProcessing}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    유효기간
                  </label>
                  <input
                    type="text"
                    value={form.expiryDate}
                    onChange={(e) =>
                      handleInputChange("expiryDate", formatExpiryDate(e.target.value))
                    }
                    placeholder="MM/YY"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    disabled={isProcessing}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    CVV
                  </label>
                  <input
                    type="text"
                    value={form.cvv}
                    onChange={(e) =>
                      handleInputChange("cvv", e.target.value.replace(/\D/g, "").slice(0, 3))
                    }
                    placeholder="123"
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                    disabled={isProcessing}
                  />
                </div>
              </div>
            </div>
          )}

          {selectedMethod === "bank_transfer" && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                계좌이체 정보는 다음 단계에서 제공됩니다.
              </p>
            </div>
          )}

          <div className="mb-6">
            <label className="flex items-start">
              <input
                type="checkbox"
                checked={form.agreeTerms}
                onChange={(e) => handleInputChange("agreeTerms", e.target.checked)}
                className="mt-1 mr-2"
                disabled={isProcessing}
              />
              <span className="text-sm text-gray-700">
                이용약관 및 개인정보 처리방침에 동의합니다. (필수)
              </span>
            </label>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={isProcessing}
            className={`w-full py-4 rounded-lg font-semibold text-white ${
              isProcessing
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {isProcessing ? "결제 처리 중..." : `₩${PLAN_PRICE.toLocaleString()} 결제하기`}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>안전한 결제를 위해 암호화된 연결을 사용합니다.</p>
          <p className="mt-1">언제든지 구독을 취소할 수 있습니다.</p>
        </div>
      </div>
    </div>
  );
}
