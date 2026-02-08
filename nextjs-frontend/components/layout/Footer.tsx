import Link from "next/link";
import { Crown, Mail, Github, Twitter, Linkedin } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-white/10 bg-slate-900">
      <div className="container mx-auto px-4 py-16">
        <div className="grid gap-12 md:grid-cols-4">
          {/* Brand */}
          <div className="md:col-span-1">
            <div className="mb-4 flex items-center gap-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-r from-blue-600 to-purple-600">
                <Crown className="h-5 w-5 text-white" />
              </div>
              <span className="bg-gradient-to-r from-white to-slate-300 bg-clip-text text-xl font-bold text-transparent">
                APT Insights
              </span>
            </div>
            <p className="mb-6 text-sm text-slate-400">
              대한민국 최고의 아파트 실거래가 분석 플랫폼
            </p>
            <div className="flex gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/5 text-slate-400 transition-colors hover:bg-white/10 hover:text-white"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/5 text-slate-400 transition-colors hover:bg-white/10 hover:text-white"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/5 text-slate-400 transition-colors hover:bg-white/10 hover:text-white"
              >
                <Linkedin className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Product */}
          <div>
            <h3 className="mb-4 font-semibold text-white">서비스</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link href="/regional" className="text-slate-400 transition-colors hover:text-white">
                  지역별 분석
                </Link>
              </li>
              <li>
                <Link href="/price-trend" className="text-slate-400 transition-colors hover:text-white">
                  가격 추이
                </Link>
              </li>
              <li>
                <Link href="/by-apartment" className="text-slate-400 transition-colors hover:text-white">
                  아파트별 분석
                </Link>
              </li>
              <li>
                <Link href="/bargain-sales" className="text-slate-400 transition-colors hover:text-white">
                  급매물 탐지
                </Link>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="mb-4 font-semibold text-white">회사</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link href="/about" className="text-slate-400 transition-colors hover:text-white">
                  회사 소개
                </Link>
              </li>
              <li>
                <Link href="/pricing" className="text-slate-400 transition-colors hover:text-white">
                  요금제
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-slate-400 transition-colors hover:text-white">
                  문의하기
                </Link>
              </li>
              <li>
                <Link href="/careers" className="text-slate-400 transition-colors hover:text-white">
                  채용
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="mb-4 font-semibold text-white">법적 고지</h3>
            <ul className="space-y-3 text-sm">
              <li>
                <Link href="/privacy" className="text-slate-400 transition-colors hover:text-white">
                  개인정보처리방침
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-slate-400 transition-colors hover:text-white">
                  이용약관
                </Link>
              </li>
              <li>
                <a
                  href="https://www.data.go.kr/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-400 transition-colors hover:text-white"
                >
                  공공데이터포털
                </a>
              </li>
              <li>
                <a
                  href="https://www.molit.go.kr/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-400 transition-colors hover:text-white"
                >
                  국토교통부
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 border-t border-white/10 pt-8">
          <div className="flex flex-col items-center justify-between gap-4 text-sm text-slate-400 md:flex-row">
            <p>
              © {currentYear} APT Insights. All rights reserved.
            </p>
            <p className="text-center md:text-right">
              국토교통부 공식 데이터 기반 • Made with ❤️ in Korea
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
