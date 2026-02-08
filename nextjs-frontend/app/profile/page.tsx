"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAuth } from "@/contexts/AuthContext";
import { User, Mail, Crown, Calendar, Clock, BarChart3, FileText, Bookmark, LogOut, Sparkles } from "lucide-react";

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
  });

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || "",
        email: user.email,
      });
    }
  }, [user]);

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-t-2 border-blue-500"></div>
          <p className="mt-4 text-slate-400">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const subscriptionConfig = {
    free: { label: "Free", color: "from-gray-500 to-slate-500", bgColor: "bg-gray-500/10", borderColor: "border-gray-500/20" },
    premium: { label: "Premium", color: "from-amber-500 to-orange-500", bgColor: "bg-amber-500/10", borderColor: "border-amber-500/20" },
    enterprise: { label: "Enterprise", color: "from-purple-500 to-pink-500", bgColor: "bg-purple-500/10", borderColor: "border-purple-500/20" },
  };

  const config = subscriptionConfig[user.subscription_tier as keyof typeof subscriptionConfig] || subscriptionConfig.free;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-600/20 via-purple-600/10 to-transparent"></div>
        <motion.div
          className="absolute left-1/3 top-20 h-96 w-96 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 opacity-10 blur-3xl"
          animate={{ y: [0, 50, 0], scale: [1, 1.2, 1] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      <div className="container relative mx-auto px-4 py-16">
        <div className="mx-auto max-w-4xl">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-12"
          >
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2">
              <User className="h-4 w-4 text-blue-400" />
              <span className="text-sm font-semibold text-blue-300">프로필</span>
            </div>
            <h1 className="mb-4 bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-5xl font-bold text-transparent">
              내 프로필
            </h1>
            <p className="text-xl text-slate-400">개인정보 및 구독 정보를 확인하세요</p>
          </motion.div>

          {/* Profile Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-8 overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 backdrop-blur-sm"
          >
            <div className="border-b border-white/10 p-8">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600">
                    <User className="h-10 w-10 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-white">{user.name || "사용자"}</h2>
                    <p className="text-slate-400">{user.email}</p>
                  </div>
                </div>
                <div className={`rounded-full border ${config.borderColor} ${config.bgColor} px-4 py-2`}>
                  <span className={`bg-gradient-to-r ${config.color} bg-clip-text text-sm font-semibold text-transparent`}>
                    {config.label}
                  </span>
                </div>
              </div>
            </div>

            <div className="p-8">
              <dl className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                    <Mail className="h-4 w-4" />
                    이메일 주소
                  </dt>
                  <dd className="text-lg text-white">{user.email}</dd>
                </div>

                <div>
                  <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                    <Crown className="h-4 w-4" />
                    구독 등급
                  </dt>
                  <dd className={`bg-gradient-to-r ${config.color} bg-clip-text text-lg font-semibold text-transparent`}>
                    {config.label}
                  </dd>
                </div>

                {user.subscription_expires_at && (
                  <div>
                    <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                      <Calendar className="h-4 w-4" />
                      구독 만료일
                    </dt>
                    <dd className="text-lg text-white">
                      {new Date(user.subscription_expires_at).toLocaleDateString("ko-KR")}
                    </dd>
                  </div>
                )}

                <div>
                  <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                    <Calendar className="h-4 w-4" />
                    가입일
                  </dt>
                  <dd className="text-lg text-white">
                    {new Date(user.created_at).toLocaleDateString("ko-KR")}
                  </dd>
                </div>

                {user.last_login_at && (
                  <div className="sm:col-span-2">
                    <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                      <Clock className="h-4 w-4" />
                      마지막 로그인
                    </dt>
                    <dd className="text-lg text-white">
                      {new Date(user.last_login_at).toLocaleString("ko-KR")}
                    </dd>
                  </div>
                )}
              </dl>
            </div>

            <div className="flex justify-between border-t border-white/10 p-6">
              <button
                type="button"
                onClick={() => setIsEditing(true)}
                disabled
                className="rounded-xl border border-white/10 bg-white/5 px-6 py-3 font-medium text-white transition-all hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
              >
                프로필 편집
              </button>

              <motion.button
                type="button"
                onClick={handleLogout}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="group relative overflow-hidden rounded-xl"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-rose-600"></div>
                <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-rose-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
                <div className="relative flex items-center gap-2 px-6 py-3 font-semibold text-white">
                  <LogOut className="h-5 w-5" />
                  로그아웃
                </div>
              </motion.button>
            </div>
          </motion.div>

          {/* Upgrade Card */}
          {user.subscription_tier === "free" && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mb-8 overflow-hidden rounded-3xl border border-amber-500/20 bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-8 backdrop-blur-sm"
            >
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-r from-amber-500 to-orange-500">
                  <Sparkles className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="mb-2 bg-gradient-to-r from-amber-200 to-orange-300 bg-clip-text text-2xl font-bold text-transparent">
                    프리미엄으로 업그레이드
                  </h3>
                  <p className="mb-4 text-amber-400/80">
                    무제한 API 호출, 고급 분석, 독점 기능을 이용하세요.
                  </p>
                  <button
                    type="button"
                    disabled
                    className="inline-flex items-center gap-2 rounded-xl border border-transparent bg-gradient-to-r from-amber-600 to-orange-600 px-6 py-3 font-semibold text-white transition-all hover:from-amber-500 hover:to-orange-500 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    <Crown className="h-5 w-5" />
                    지금 업그레이드
                  </button>
                </div>
              </div>
            </motion.div>
          )}

          {/* Statistics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 to-white/0 p-8 backdrop-blur-sm"
          >
            <h3 className="mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-2xl font-bold text-transparent">
              계정 통계
            </h3>
            <dl className="grid grid-cols-1 gap-6 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                  <BarChart3 className="h-4 w-4" />
                  오늘 API 호출
                </dt>
                <dd className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-3xl font-bold text-transparent">
                  {user.subscription_tier === "free" ? "5/10" : "무제한"}
                </dd>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                  <FileText className="h-4 w-4" />
                  생성된 리포트
                </dt>
                <dd className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-3xl font-bold text-transparent">
                  12
                </dd>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <dt className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-400">
                  <Bookmark className="h-4 w-4" />
                  저장된 검색
                </dt>
                <dd className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-3xl font-bold text-transparent">
                  3
                </dd>
              </div>
            </dl>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
