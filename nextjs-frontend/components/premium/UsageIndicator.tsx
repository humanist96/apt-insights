'use client';

import React from 'react';
import { useSubscription } from '@/contexts/SubscriptionContext';
import PremiumBadge from './PremiumBadge';
import Link from 'next/link';

export default function UsageIndicator() {
  const { subscription, isPremium, isLoading } = useSubscription();

  if (isLoading || !subscription) {
    return (
      <div className="flex items-center gap-2">
        <div className="h-8 w-24 animate-pulse rounded-full bg-gray-200" />
      </div>
    );
  }

  if (isPremium) {
    return (
      <Link
        href="/subscription"
        className="flex items-center gap-2 rounded-full bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-2 text-sm font-semibold text-white transition-opacity hover:opacity-90"
      >
        <PremiumBadge size="sm" className="bg-white/20" />
        <span>무제한</span>
      </Link>
    );
  }

  const { used, limit, percentage } = subscription.usage;

  let colorClasses = 'bg-green-100 text-green-800 border-green-200';
  if (percentage >= 80) {
    colorClasses = 'bg-red-100 text-red-800 border-red-200';
  } else if (percentage >= 50) {
    colorClasses = 'bg-yellow-100 text-yellow-800 border-yellow-200';
  }

  return (
    <Link
      href="/subscription"
      className={`flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-medium transition-opacity hover:opacity-80 ${colorClasses}`}
    >
      <span>
        API: {used}/{limit}
      </span>
      {percentage >= 80 && (
        <svg
          className="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
      )}
    </Link>
  );
}
