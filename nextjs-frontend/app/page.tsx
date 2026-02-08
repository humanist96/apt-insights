"use client";

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
  LineChart,
  Sparkles,
  Crown,
  Award,
  Star
} from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  };

  const staggerContainer = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Premium Hero Section */}
      <section className="relative overflow-hidden py-32">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-600/20 via-purple-600/10 to-transparent"></div>
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-5"></div>
          {/* Floating Orbs */}
          <motion.div
            className="absolute left-1/4 top-20 h-64 w-64 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 opacity-20 blur-3xl"
            animate={{
              y: [0, 30, 0],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <motion.div
            className="absolute right-1/4 top-40 h-96 w-96 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 opacity-10 blur-3xl"
            animate={{
              y: [0, -40, 0],
              scale: [1, 1.2, 1],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        </div>

        <div className="container relative mx-auto px-4">
          <motion.div
            className="mx-auto max-w-5xl text-center"
            initial="initial"
            animate="animate"
            variants={staggerContainer}
          >
            {/* Premium Badge */}
            <motion.div variants={fadeInUp} className="mb-8 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-gradient-to-r from-amber-500/10 to-amber-600/10 px-6 py-3 backdrop-blur-sm">
              <Crown className="h-5 w-5 text-amber-400" />
              <span className="bg-gradient-to-r from-amber-200 to-amber-400 bg-clip-text text-sm font-semibold text-transparent">
                Premium Real Estate Analytics Platform
              </span>
            </motion.div>

            <motion.h1
              variants={fadeInUp}
              className="mb-8 bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-6xl font-bold leading-tight text-transparent md:text-7xl lg:text-8xl"
            >
              아파트 투자의
              <br />
              새로운 기준
            </motion.h1>

            <motion.p
              variants={fadeInUp}
              className="mb-12 text-2xl text-slate-300 md:text-3xl"
            >
              63,809건의 실거래가 데이터로
              <br className="hidden md:block" />
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text font-semibold text-transparent">
                스마트한 투자 결정
              </span>을 내리세요
            </motion.p>

            <motion.div
              variants={fadeInUp}
              className="flex flex-col justify-center gap-6 sm:flex-row"
            >
              <Link href="/register">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="group relative overflow-hidden rounded-2xl"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-blue-500 to-purple-600"></div>
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
                  <div className="relative flex items-center gap-2 px-10 py-5 text-lg font-semibold text-white">
                    <Sparkles className="h-5 w-5" />
                    무료로 시작하기
                    <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
                  </div>
                </motion.div>
              </Link>

              <Link href="/regional">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="group relative overflow-hidden rounded-2xl"
                >
                  <div className="absolute inset-0 bg-white/5 backdrop-blur-sm"></div>
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
                  <div className="relative flex items-center gap-2 border-2 border-white/20 px-10 py-5 text-lg font-semibold text-white">
                    <LineChart className="h-5 w-5" />
                    데모 체험하기
                  </div>
                </motion.div>
              </Link>
            </motion.div>

            <motion.div
              variants={fadeInUp}
              className="mt-12 flex items-center justify-center gap-6 text-sm text-slate-400"
            >
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400" />
                신용카드 등록 불필요
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-400" />
                언제든 취소 가능
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Premium Stats Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid grid-cols-2 gap-6 md:grid-cols-4"
          >
            {[
              { value: "63,809", label: "실거래 데이터", icon: BarChart3, gradient: "from-blue-500 to-cyan-500" },
              { value: "12+", label: "프리미엄 분석 도구", icon: Target, gradient: "from-purple-500 to-pink-500" },
              { value: "실시간", label: "데이터 업데이트", icon: Zap, gradient: "from-amber-500 to-orange-500" },
              { value: "100%", label: "국토부 공식 데이터", icon: Shield, gradient: "from-green-500 to-emerald-500" }
            ].map((stat, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-8 backdrop-blur-sm transition-all duration-300 hover:border-white/20 hover:from-white/10"
              >
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r ${stat.gradient} opacity-80`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <div className={`mb-2 bg-gradient-to-r ${stat.gradient} bg-clip-text text-4xl font-bold text-transparent`}>
                  {stat.value}
                </div>
                <div className="text-sm text-slate-400">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Premium Features Section */}
      <section className="py-32">
        <div className="container mx-auto px-4">
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="mb-20 text-center"
          >
            <motion.div variants={fadeInUp} className="mb-6 inline-flex items-center gap-2 rounded-full border border-purple-500/20 bg-purple-500/10 px-4 py-2">
              <Award className="h-4 w-4 text-purple-400" />
              <span className="text-sm font-semibold text-purple-300">프리미엄 기능</span>
            </motion.div>
            <motion.h2
              variants={fadeInUp}
              className="mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-5xl font-bold text-transparent md:text-6xl"
            >
              투자 성공을 위한
              <br />
              모든 것
            </motion.h2>
            <motion.p
              variants={fadeInUp}
              className="text-xl text-slate-400"
            >
              전문가 수준의 부동산 분석을 누구나 쉽게
            </motion.p>
          </motion.div>

          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="grid gap-8 md:grid-cols-3"
          >
            {[
              {
                icon: Zap,
                title: "실시간 분석",
                description: "국토교통부 최신 실거래가 데이터를 실시간으로 분석하여 시장 트렌드를 빠르게 파악하세요.",
                gradient: "from-blue-500 to-cyan-500"
              },
              {
                icon: TrendingUp,
                title: "AI 기반 예측",
                description: "머신러닝 알고리즘으로 향후 가격 추이를 예측하고 투자 타이밍을 놓치지 마세요.",
                gradient: "from-purple-500 to-pink-500"
              },
              {
                icon: Target,
                title: "맞춤형 포트폴리오",
                description: "보유 부동산을 관리하고 실시간 평가손익을 확인하며 전문가처럼 투자하세요.",
                gradient: "from-amber-500 to-orange-500"
              },
              {
                icon: Shield,
                title: "안전한 투자",
                description: "깡통전세 위험도 분석과 전세가율 모니터링으로 안전한 투자를 보장합니다.",
                gradient: "from-green-500 to-emerald-500"
              },
              {
                icon: BarChart3,
                title: "심화 분석 리포트",
                description: "PDF/CSV 다운로드로 상세한 투자 리포트를 받아보고 의사결정에 활용하세요.",
                gradient: "from-rose-500 to-pink-500"
              },
              {
                icon: Star,
                title: "프리미엄 지원",
                description: "전문 부동산 애널리스트의 1:1 상담과 맞춤형 투자 전략을 제공받으세요.",
                gradient: "from-indigo-500 to-purple-500"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                whileHover={{ y: -10 }}
                className="group relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-8 backdrop-blur-sm transition-all duration-300"
              >
                {/* Glow Effect */}
                <div className={`absolute -inset-1 bg-gradient-to-r ${feature.gradient} opacity-0 blur-xl transition-opacity duration-300 group-hover:opacity-30`}></div>

                <div className="relative">
                  <div className={`mb-6 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-r ${feature.gradient}`}>
                    <feature.icon className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="mb-4 text-2xl font-bold text-white">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400">
                    {feature.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Premium CTA Section */}
      <section className="py-32">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-blue-600/20 via-purple-600/20 to-pink-600/20 p-16 backdrop-blur-sm"
          >
            {/* Animated Background */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10"></div>

            <div className="relative mx-auto max-w-4xl text-center">
              <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/10 px-6 py-3">
                <Crown className="h-5 w-5 text-amber-400" />
                <span className="text-sm font-semibold text-amber-300">Limited Time Offer</span>
              </div>

              <h2 className="mb-6 bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-5xl font-bold text-transparent md:text-6xl">
                지금 시작하고
                <br />
                첫 달 무료 혜택 받기
              </h2>

              <p className="mb-12 text-xl text-slate-300">
                프리미엄 멤버십으로 모든 기능을 제한 없이 사용하세요
              </p>

              <Link href="/register">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex"
                >
                  <div className="group relative overflow-hidden rounded-2xl">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600"></div>
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
                    <div className="relative flex items-center gap-3 px-12 py-6 text-xl font-bold text-white">
                      <Sparkles className="h-6 w-6" />
                      지금 바로 시작하기
                      <ArrowRight className="h-6 w-6 transition-transform group-hover:translate-x-2" />
                    </div>
                  </div>
                </motion.div>
              </Link>

              <div className="mt-8 flex items-center justify-center gap-8 text-sm text-slate-400">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400" />
                  첫 달 완전 무료
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400" />
                  언제든 해지 가능
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-400" />
                  모든 프리미엄 기능
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
