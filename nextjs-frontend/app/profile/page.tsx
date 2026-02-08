'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  });

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name || '',
        email: user.email,
      });
    }
  }, [user]);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const subscriptionTierDisplay = {
    free: 'Free',
    premium: 'Premium',
    enterprise: 'Enterprise',
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Profile</h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Personal details and subscription information
            </p>
          </div>

          <div className="px-4 py-5 sm:p-6">
            <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
              <div className="sm:col-span-1">
                <dt className="text-sm font-medium text-gray-500">Full name</dt>
                <dd className="mt-1 text-sm text-gray-900">{user.name || 'Not set'}</dd>
              </div>

              <div className="sm:col-span-1">
                <dt className="text-sm font-medium text-gray-500">Email address</dt>
                <dd className="mt-1 text-sm text-gray-900">{user.email}</dd>
              </div>

              <div className="sm:col-span-1">
                <dt className="text-sm font-medium text-gray-500">Subscription tier</dt>
                <dd className="mt-1">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      user.subscription_tier === 'premium'
                        ? 'bg-yellow-100 text-yellow-800'
                        : user.subscription_tier === 'enterprise'
                        ? 'bg-purple-100 text-purple-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {subscriptionTierDisplay[user.subscription_tier as keyof typeof subscriptionTierDisplay] || user.subscription_tier}
                  </span>
                </dd>
              </div>

              {user.subscription_expires_at && (
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Subscription expires</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {new Date(user.subscription_expires_at).toLocaleDateString()}
                  </dd>
                </div>
              )}

              <div className="sm:col-span-1">
                <dt className="text-sm font-medium text-gray-500">Member since</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {new Date(user.created_at).toLocaleDateString()}
                </dd>
              </div>

              {user.last_login_at && (
                <div className="sm:col-span-1">
                  <dt className="text-sm font-medium text-gray-500">Last login</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {new Date(user.last_login_at).toLocaleString()}
                  </dd>
                </div>
              )}
            </dl>
          </div>

          <div className="px-4 py-3 sm:px-6 bg-gray-50 border-t border-gray-200 flex justify-between">
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              disabled
              className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Edit profile
            </button>

            <button
              type="button"
              onClick={handleLogout}
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Sign out
            </button>
          </div>
        </div>

        {user.subscription_tier === 'free' && (
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h4 className="text-lg font-medium text-blue-900 mb-2">Upgrade to Premium</h4>
            <p className="text-sm text-blue-700 mb-4">
              Unlock unlimited API calls, advanced analytics, and exclusive features.
            </p>
            <button
              type="button"
              disabled
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Upgrade now
            </button>
          </div>
        )}

        <div className="mt-6 bg-white shadow rounded-lg p-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">Account Statistics</h4>
          <dl className="grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div className="bg-gray-50 px-4 py-5 rounded-lg">
              <dt className="text-sm font-medium text-gray-500 truncate">API Calls Today</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">
                {user.subscription_tier === 'free' ? '5/10' : 'Unlimited'}
              </dd>
            </div>
            <div className="bg-gray-50 px-4 py-5 rounded-lg">
              <dt className="text-sm font-medium text-gray-500 truncate">Reports Generated</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">12</dd>
            </div>
            <div className="bg-gray-50 px-4 py-5 rounded-lg">
              <dt className="text-sm font-medium text-gray-500 truncate">Saved Searches</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">3</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  );
}
