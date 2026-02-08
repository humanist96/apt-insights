'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { subscriptionApi, UserSubscription, SubscriptionPlan } from '@/lib/api/subscriptions';

interface SubscriptionContextValue {
  subscription: UserSubscription | null;
  plans: SubscriptionPlan[];
  isLoading: boolean;
  isPremium: boolean;
  refreshSubscription: () => Promise<void>;
  upgrade: (planId: string) => Promise<{ success: boolean; message: string }>;
  cancel: () => Promise<{ success: boolean; message: string }>;
  checkFeatureAccess: (feature: keyof SubscriptionPlan['features']) => boolean;
}

const SubscriptionContext = createContext<SubscriptionContextValue | undefined>(undefined);

export function SubscriptionProvider({ children }: { children: ReactNode }) {
  const [subscription, setSubscription] = useState<UserSubscription | null>(null);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchSubscription = async () => {
    try {
      const [currentSub, availablePlans] = await Promise.all([
        subscriptionApi.getCurrentSubscription(),
        subscriptionApi.getPlans(),
      ]);
      setSubscription(currentSub);
      setPlans(availablePlans);
    } catch (error) {
      console.error('Failed to fetch subscription:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSubscription();
  }, []);

  const refreshSubscription = async () => {
    await fetchSubscription();
  };

  const upgrade = async (planId: string) => {
    try {
      const result = await subscriptionApi.upgrade({ plan_id: planId });
      await refreshSubscription();
      return result;
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.detail || '업그레이드 실패',
      };
    }
  };

  const cancel = async () => {
    try {
      const result = await subscriptionApi.cancel();
      await refreshSubscription();
      return result;
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.detail || '취소 실패',
      };
    }
  };

  const checkFeatureAccess = (feature: keyof SubscriptionPlan['features']): boolean => {
    if (!subscription) {
      return false;
    }
    const featureValue = subscription.features[feature];
    return typeof featureValue === 'boolean' ? featureValue : featureValue !== 0;
  };

  const isPremium = subscription?.tier === 'premium';

  const value: SubscriptionContextValue = {
    subscription,
    plans,
    isLoading,
    isPremium,
    refreshSubscription,
    upgrade,
    cancel,
    checkFeatureAccess,
  };

  return (
    <SubscriptionContext.Provider value={value}>
      {children}
    </SubscriptionContext.Provider>
  );
}

export function useSubscription() {
  const context = useContext(SubscriptionContext);
  if (context === undefined) {
    throw new Error('useSubscription must be used within a SubscriptionProvider');
  }
  return context;
}
