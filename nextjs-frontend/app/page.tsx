import Link from "next/link";
import Button from "@/components/ui/Button";
import {
  TrendingUp,
  BarChart3,
  Target,
  CheckCircle,
  ArrowRight,
  Zap,
  Shield,
  LineChart
} from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 py-20 text-white">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="container relative mx-auto px-4">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="mb-6 text-5xl font-bold leading-tight md:text-6xl">
              아파트 투자,<br />이제 데이터로 결정하세요
            </h1>
            <p className="mb-8 text-xl text-blue-100 md:text-2xl">
              63,809건의 실거래가 데이터 분석으로 스마트한 투자 결정
            </p>
            <div className="flex flex-col justify-center gap-4 sm:flex-row">
              <Link href="/register">
                <Button
                  variant="primary"
                  className="h-14 bg-white px-8 text-lg text-blue-700 hover:bg-blue-50"
                >
                  무료로 시작하기
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/regional">
                <Button
                  variant="secondary"
                  className="h-14 border-2 border-white bg-transparent px-8 text-lg text-white hover:bg-white/10"
                >
                  데모 보기
                </Button>
              </Link>
            </div>
            <div className="mt-8 text-sm text-blue-200">
              신용카드 등록 불필요 • 언제든 취소 가능
            </div>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="border-b bg-gray-50 py-8 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 gap-8 text-center md:grid-cols-4">
            <div>
              <div className="text-3xl font-bold text-blue-600">63,809</div>
              <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">실거래 데이터</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">12+</div>
              <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">분석 도구</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">실시간</div>
              <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">데이터 업데이트</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">100%</div>
              <div className="mt-1 text-sm text-gray-600 dark:text-gray-400">국토부 공식 데이터</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-4xl font-bold">투자 성공을 위한 모든 도구</h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              전문가 수준의 부동산 분석을 누구나 쉽게
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            <div className="rounded-lg border bg-white p-8 shadow-sm transition-shadow hover:shadow-lg dark:bg-gray-800">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-600 dark:bg-blue-900">
                <Zap className="h-6 w-6" />
              </div>
              <h3 className="mb-3 text-xl font-bold">실시간 분석</h3>
              <p className="text-gray-600 dark:text-gray-400">
                국토교통부 최신 실거래가 데이터를 실시간으로 분석하여 시장 트렌드를 빠르게 파악하세요.
              </p>
            </div>

            <div className="rounded-lg border bg-white p-8 shadow-sm transition-shadow hover:shadow-lg dark:bg-gray-800">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-green-100 text-green-600 dark:bg-green-900">
                <BarChart3 className="h-6 w-6" />
              </div>
              <h3 className="mb-3 text-xl font-bold">심층 인사이트</h3>
              <p className="text-gray-600 dark:text-gray-400">
                12가지 전문가급 분석 도구로 지역별, 평형별, 시기별 세밀한 시장 분석이 가능합니다.
              </p>
            </div>

            <div className="rounded-lg border bg-white p-8 shadow-sm transition-shadow hover:shadow-lg dark:bg-gray-800">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900">
                <Target className="h-6 w-6" />
              </div>
              <h3 className="mb-3 text-xl font-bold">투자 기회 발굴</h3>
              <p className="text-gray-600 dark:text-gray-400">
                갭투자, 급매물, 저평가 아파트를 자동으로 탐지하여 투자 기회를 놓치지 마세요.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gray-50 py-20 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-4xl font-bold">어떻게 작동하나요?</h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              3단계로 시작하는 스마트한 투자
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            <div className="text-center">
              <div className="mb-6 flex justify-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-2xl font-bold text-white">
                  1
                </div>
              </div>
              <h3 className="mb-3 text-xl font-bold">관심 지역 선택</h3>
              <p className="text-gray-600 dark:text-gray-400">
                투자하고 싶은 지역을 선택하면 해당 지역의 모든 실거래 데이터를 불러옵니다.
              </p>
            </div>

            <div className="text-center">
              <div className="mb-6 flex justify-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-2xl font-bold text-white">
                  2
                </div>
              </div>
              <h3 className="mb-3 text-xl font-bold">다양한 분석 도구 활용</h3>
              <p className="text-gray-600 dark:text-gray-400">
                가격 트렌드, 거래량, 갭투자, 급매물 등 12가지 분석 메뉴를 활용하세요.
              </p>
            </div>

            <div className="text-center">
              <div className="mb-6 flex justify-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-2xl font-bold text-white">
                  3
                </div>
              </div>
              <h3 className="mb-3 text-xl font-bold">데이터 기반 투자 결정</h3>
              <p className="text-gray-600 dark:text-gray-400">
                분석 결과를 바탕으로 자신감 있는 투자 결정을 내리세요.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-4xl font-bold">투명한 가격 정책</h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              필요한 만큼만 결제하세요
            </p>
          </div>

          <div className="mx-auto grid max-w-5xl gap-8 md:grid-cols-2">
            {/* Free Plan */}
            <div className="rounded-lg border-2 bg-white p-8 shadow-sm dark:bg-gray-800">
              <div className="mb-4">
                <h3 className="text-2xl font-bold">무료</h3>
                <div className="mt-2">
                  <span className="text-4xl font-bold">₩0</span>
                  <span className="text-gray-600 dark:text-gray-400">/월</span>
                </div>
              </div>
              <ul className="mb-8 space-y-3">
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-green-500" />
                  <span>월 10회 데이터 조회</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-green-500" />
                  <span>기본 분석 도구</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-green-500" />
                  <span>최근 3개월 데이터</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-green-500" />
                  <span>웹 대시보드 접근</span>
                </li>
              </ul>
              <Link href="/register">
                <Button variant="secondary" className="w-full">
                  무료로 시작하기
                </Button>
              </Link>
            </div>

            {/* Premium Plan */}
            <div className="relative rounded-lg border-2 border-blue-600 bg-white p-8 shadow-lg dark:bg-gray-800">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-blue-600 px-4 py-1 text-sm font-bold text-white">
                추천
              </div>
              <div className="mb-4">
                <h3 className="text-2xl font-bold">프리미엄</h3>
                <div className="mt-2">
                  <span className="text-4xl font-bold">₩29,000</span>
                  <span className="text-gray-600 dark:text-gray-400">/월</span>
                </div>
              </div>
              <ul className="mb-8 space-y-3">
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <span className="font-semibold">무제한 데이터 조회</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <span className="font-semibold">모든 고급 분석 도구</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <span className="font-semibold">5년 과거 데이터 접근</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <span className="font-semibold">CSV/PDF 데이터 내보내기</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <span className="font-semibold">갭투자 기회 알림</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-600" />
                  <span className="font-semibold">우선 고객 지원</span>
                </li>
              </ul>
              <Link href="/payment">
                <Button variant="primary" className="w-full">
                  프리미엄 시작하기
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="bg-gray-50 py-20 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-4xl font-bold">고객 후기</h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              실제 사용자들의 생생한 경험담
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            <div className="rounded-lg bg-white p-6 shadow-sm dark:bg-gray-800">
              <div className="mb-4 flex items-center">
                <div className="mr-3 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600">
                  김
                </div>
                <div>
                  <div className="font-bold">김민수</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">서울 강남구 투자자</div>
                </div>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                "갭투자 기회를 찾는데 정말 유용해요. 실거래가 데이터로 저평가된 매물을 쉽게 찾을 수 있었습니다."
              </p>
            </div>

            <div className="rounded-lg bg-white p-6 shadow-sm dark:bg-gray-800">
              <div className="mb-4 flex items-center">
                <div className="mr-3 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600">
                  이
                </div>
                <div>
                  <div className="font-bold">이지은</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">경기 수원시 투자자</div>
                </div>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                "복잡한 부동산 데이터를 한눈에 볼 수 있어서 좋아요. 초보자도 쉽게 이해할 수 있는 시각화가 인상적입니다."
              </p>
            </div>

            <div className="rounded-lg bg-white p-6 shadow-sm dark:bg-gray-800">
              <div className="mb-4 flex items-center">
                <div className="mr-3 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-purple-600">
                  박
                </div>
                <div>
                  <div className="font-bold">박준호</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">서울 송파구 투자자</div>
                </div>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                "전세가율 분석으로 깡통전세를 피할 수 있었어요. 안전한 투자에 꼭 필요한 도구입니다."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-4xl font-bold">자주 묻는 질문</h2>
          </div>

          <div className="mx-auto max-w-3xl space-y-4">
            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                데이터는 얼마나 자주 업데이트되나요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                국토교통부 공공데이터 API를 통해 실시간으로 데이터를 수집합니다.
                실거래가 신고가 접수되는 즉시 플랫폼에 반영됩니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                무료 플랜과 프리미엄의 차이는 무엇인가요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                무료 플랜은 월 10회 조회 제한과 최근 3개월 데이터만 제공됩니다.
                프리미엄은 무제한 조회, 5년 과거 데이터, 고급 분석 도구, 데이터 내보내기 기능을 제공합니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                결제는 어떻게 이루어지나요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                신용카드, 체크카드, 간편결제(카카오페이, 네이버페이 등)를 지원합니다.
                언제든지 구독을 취소할 수 있으며, 별도의 위약금은 없습니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                어떤 지역의 데이터를 볼 수 있나요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                전국 모든 시·군·구의 아파트 실거래가 데이터를 제공합니다.
                서울, 경기, 인천을 포함한 수도권은 물론 지방 광역시와 중소도시까지 전부 조회 가능합니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                갭투자란 무엇인가요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                갭투자는 전세가와 매매가의 차이(갭)가 적은 매물에 투자하는 전략입니다.
                적은 자본으로 부동산을 보유할 수 있어 초보 투자자에게 인기가 많습니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                환불 정책은 어떻게 되나요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                프리미엄 구독 후 7일 이내에는 전액 환불이 가능합니다.
                그 이후에는 언제든 구독을 취소할 수 있으며, 다음 결제일에 자동으로 종료됩니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                모바일에서도 사용할 수 있나요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                네, 반응형 웹 디자인으로 PC, 태블릿, 스마트폰 모두에서 최적화된 경험을 제공합니다.
                별도의 앱 설치 없이 웹브라우저에서 바로 사용하실 수 있습니다.
              </p>
            </details>

            <details className="group rounded-lg border bg-white p-6 dark:bg-gray-800">
              <summary className="cursor-pointer text-lg font-bold">
                고객 지원은 어떻게 받나요?
              </summary>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                이메일(support@aptanalysis.com)로 문의하실 수 있으며,
                프리미엄 회원은 우선 지원을 받으실 수 있습니다. 평균 24시간 이내 답변을 드립니다.
              </p>
            </details>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-br from-blue-600 to-indigo-700 py-20 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="mb-4 text-4xl font-bold">지금 바로 시작하세요</h2>
          <p className="mb-8 text-xl text-blue-100">
            무료로 시작하고, 필요할 때 업그레이드하세요
          </p>
          <div className="flex flex-col justify-center gap-4 sm:flex-row">
            <Link href="/register">
              <Button
                variant="primary"
                className="h-14 bg-white px-8 text-lg text-blue-700 hover:bg-blue-50"
              >
                무료 계정 만들기
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/regional">
              <Button
                variant="secondary"
                className="h-14 border-2 border-white bg-transparent px-8 text-lg text-white hover:bg-white/10"
              >
                먼저 둘러보기
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
