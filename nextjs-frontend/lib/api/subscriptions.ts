import { apiClient } from '../api-client';

export interface SubscriptionPlan {
  plan_id: string;
  name: string;
  tier: 'free' | 'premium';
  price_monthly: number;
  price_yearly: number | null;
  features: {
    api_calls_per_day: number | null;
    basic_analysis: boolean;
    csv_export: boolean;
    pdf_export: boolean;
    portfolio_tracking: boolean;
    price_alerts: boolean;
    max_portfolios: number;
    max_alerts: number;
  };
  description: string;
  popular: boolean;
}

export interface UserSubscription {
  user_id: string;
  tier: 'free' | 'premium';
  plan_name: string;
  expires_at: string | null;
  features: SubscriptionPlan['features'];
  usage: {
    used: number;
    limit: number | null;
    remaining: number | null;
    percentage: number;
    unlimited: boolean;
  };
}

export interface UpgradeRequest {
  plan_id: string;
  payment_method?: string;
}

export interface ExportRequest {
  export_type: 'csv' | 'pdf';
  filters?: Record<string, any>;
  fields?: string[];
}

export const subscriptionApi = {
  async getPlans(): Promise<SubscriptionPlan[]> {
    const response = await apiClient.get('/api/v1/subscriptions/plans');
    return response.data.data;
  },

  async getCurrentSubscription(): Promise<UserSubscription> {
    const response = await apiClient.get('/api/v1/subscriptions/current');
    return response.data.data;
  },

  async upgrade(request: UpgradeRequest): Promise<{ success: boolean; message: string; data: any }> {
    const response = await apiClient.post('/api/v1/subscriptions/upgrade', request);
    return response.data;
  },

  async cancel(): Promise<{ success: boolean; message: string }> {
    const response = await apiClient.post('/api/v1/subscriptions/cancel');
    return response.data;
  },

  async getUsageStats(): Promise<UserSubscription['usage']> {
    const response = await apiClient.get('/api/v1/subscriptions/usage');
    return response.data.data;
  },

  async exportCsv(request: ExportRequest): Promise<Blob> {
    const response = await apiClient.post('/api/v1/export/csv', request, {
      responseType: 'blob',
    });
    return response.data;
  },

  async exportPdf(request: ExportRequest): Promise<{ success: boolean; filename: string; message?: string }> {
    const response = await apiClient.post('/api/v1/export/pdf', request);
    return response.data;
  },
};
