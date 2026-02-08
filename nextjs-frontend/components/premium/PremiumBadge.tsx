import React from 'react';

interface PremiumBadgeProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export default function PremiumBadge({ size = 'md', className = '' }: PremiumBadgeProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-1.5',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full bg-gradient-to-r from-amber-500 to-orange-500 font-semibold text-white ${sizeClasses[size]} ${className}`}
    >
      Premium
    </span>
  );
}
