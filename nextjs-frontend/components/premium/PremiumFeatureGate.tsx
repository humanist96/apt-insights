'use client';

import React, { ReactNode, useState } from 'react';
import { useSubscription } from '@/contexts/SubscriptionContext';
import UpgradeModal from './UpgradeModal';
import PremiumBadge from './PremiumBadge';

interface PremiumFeatureGateProps {
  feature: 'csv_export' | 'pdf_export' | 'portfolio_tracking' | 'price_alerts';
  featureName: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export default function PremiumFeatureGate({
  feature,
  featureName,
  children,
  fallback,
}: PremiumFeatureGateProps) {
  const { checkFeatureAccess } = useSubscription();
  const [showModal, setShowModal] = useState(false);

  const hasAccess = checkFeatureAccess(feature);

  if (hasAccess) {
    return <>{children}</>;
  }

  const handleClick = () => {
    setShowModal(true);
  };

  if (fallback) {
    return (
      <>
        <div onClick={handleClick} role="button" tabIndex={0}>
          {fallback}
        </div>
        <UpgradeModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          featureName={featureName}
        />
      </>
    );
  }

  return (
    <>
      <div
        className="relative cursor-pointer"
        onClick={handleClick}
        role="button"
        tabIndex={0}
      >
        <div className="pointer-events-none opacity-50">{children}</div>
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80">
          <div className="rounded-lg bg-white p-4 text-center shadow-lg">
            <PremiumBadge size="md" className="mb-2" />
            <p className="text-sm text-gray-700">
              프리미엄 전용 기능
            </p>
          </div>
        </div>
      </div>
      <UpgradeModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        featureName={featureName}
      />
    </>
  );
}
