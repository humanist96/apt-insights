'use client';

import { MarketSignal } from '@/types/analysis';
import { AlertTriangle, AlertCircle, Info } from 'lucide-react';

interface MarketSignalCardProps {
  signal: MarketSignal;
}

const signalConfig = {
  strong: {
    bgColor: 'bg-red-50 dark:bg-red-900/20',
    borderColor: 'border-red-200 dark:border-red-800',
    textColor: 'text-red-900 dark:text-red-300',
    detailColor: 'text-red-700 dark:text-red-400',
    icon: AlertTriangle,
    iconColor: 'text-red-600',
  },
  moderate: {
    bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
    borderColor: 'border-yellow-200 dark:border-yellow-800',
    textColor: 'text-yellow-900 dark:text-yellow-300',
    detailColor: 'text-yellow-700 dark:text-yellow-400',
    icon: AlertCircle,
    iconColor: 'text-yellow-600',
  },
  weak: {
    bgColor: 'bg-blue-50 dark:bg-blue-900/20',
    borderColor: 'border-blue-200 dark:border-blue-800',
    textColor: 'text-blue-900 dark:text-blue-300',
    detailColor: 'text-blue-700 dark:text-blue-400',
    icon: Info,
    iconColor: 'text-blue-600',
  },
};

export default function MarketSignalCard({ signal }: MarketSignalCardProps) {
  const config = signalConfig[signal.level];
  const Icon = config.icon;

  return (
    <div
      className={`${config.bgColor} ${config.borderColor} border rounded-lg p-4`}
    >
      <div className="flex items-start gap-3">
        <Icon className={`${config.iconColor} h-5 w-5 mt-0.5 flex-shrink-0`} />
        <div className="flex-1 min-w-0">
          <h4 className={`font-semibold ${config.textColor} mb-1`}>
            {signal.title}
          </h4>
          <p className={`text-sm ${config.detailColor}`}>
            {signal.detail}
          </p>
        </div>
      </div>
    </div>
  );
}
