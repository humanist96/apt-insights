'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Card from '@/components/ui/Card';
import CollectionConfig from '@/components/admin/CollectionConfig';
import CollectionProgressComponent from '@/components/admin/CollectionProgress';
import CollectionHistory from '@/components/admin/CollectionHistory';
import { useBatchCollection } from '@/hooks/useBatchCollection';
import { CollectionConfig as CollectionConfigType } from '@/types/batch-collection';
import { getMockCollectionStatistics } from '@/lib/batch-collection-mock';

export default function BatchCollectionPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(true);
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState('');
  const [config, setConfig] = useState<CollectionConfigType | null>(null);
  const [isConfigValid, setIsConfigValid] = useState(false);

  const { isCollecting, progress, startCollection, cancelCollection, getCollectionHistory } =
    useBatchCollection();

  const history = getCollectionHistory();
  const statistics = getMockCollectionStatistics(history);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const auth = localStorage.getItem('adminAuth');
      if (auth === 'authenticated') {
        setIsAuthenticated(true);
      }
    }
    setIsAuthenticating(false);
  }, []);

  const handleAuth = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === 'admin123') {
      if (typeof window !== 'undefined') {
        localStorage.setItem('adminAuth', 'authenticated');
      }
      setIsAuthenticated(true);
      setAuthError('');
    } else {
      setAuthError('비밀번호가 올바르지 않습니다.');
    }
  };

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('adminAuth');
    }
    setIsAuthenticated(false);
    setPassword('');
  };

  const handleConfigChange = (newConfig: CollectionConfigType) => {
    setConfig(newConfig);
    setIsConfigValid(
      newConfig.regions.length > 0 &&
        newConfig.apis.length > 0 &&
        newConfig.startMonth <= newConfig.endMonth
    );
  };

  const handleStartCollection = async () => {
    if (!config || !isConfigValid) {
      return;
    }
    await startCollection(config);
  };

  if (isAuthenticating) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-gray-600 dark:text-gray-400">로딩 중...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="w-full max-w-md">
          <Card title="관리자 인증">
            <form onSubmit={handleAuth} className="space-y-4">
              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                  비밀번호
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-gray-300 p-2.5 text-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
                  placeholder="관리자 비밀번호를 입력하세요"
                  autoFocus
                />
              </div>
              {authError && (
                <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600 dark:bg-red-900/20 dark:text-red-400">
                  {authError}
                </div>
              )}
              <button
                type="submit"
                className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                로그인
              </button>
              <div className="text-center">
                <button
                  type="button"
                  onClick={() => router.push('/')}
                  className="text-sm text-gray-600 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
                >
                  홈으로 돌아가기
                </button>
              </div>
            </form>
          </Card>
          <div className="mt-4 text-center text-xs text-gray-500 dark:text-gray-400">
            데모 비밀번호: admin123
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            배치 데이터 수집
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            여러 지역과 기간에 대한 아파트 실거래가 데이터를 일괄 수집합니다
          </p>
        </div>
        <button
          type="button"
          onClick={handleLogout}
          className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
        >
          로그아웃
        </button>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">
        <div className="rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 p-6 text-white shadow-lg">
          <div className="text-sm opacity-90">총 수집 횟수</div>
          <div className="mt-2 text-3xl font-bold">
            {statistics.totalCollections.toLocaleString()}
          </div>
        </div>
        <div className="rounded-lg bg-gradient-to-br from-green-500 to-green-600 p-6 text-white shadow-lg">
          <div className="text-sm opacity-90">성공</div>
          <div className="mt-2 text-3xl font-bold">
            {statistics.successfulCollections.toLocaleString()}
          </div>
        </div>
        <div className="rounded-lg bg-gradient-to-br from-red-500 to-red-600 p-6 text-white shadow-lg">
          <div className="text-sm opacity-90">실패</div>
          <div className="mt-2 text-3xl font-bold">
            {statistics.failedCollections.toLocaleString()}
          </div>
        </div>
        <div className="rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 p-6 text-white shadow-lg">
          <div className="text-sm opacity-90">총 레코드</div>
          <div className="mt-2 text-3xl font-bold">
            {statistics.totalRecordsCollected.toLocaleString()}
          </div>
        </div>
      </div>

      {!isCollecting && !progress && (
        <>
          <div className="mb-6">
            <CollectionConfig
              onConfigChange={handleConfigChange}
              disabled={isCollecting}
            />
          </div>

          <div className="mb-6">
            <button
              type="button"
              onClick={handleStartCollection}
              disabled={!isConfigValid || isCollecting}
              className="w-full rounded-lg bg-blue-600 px-6 py-3 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400 dark:bg-blue-500 dark:hover:bg-blue-600 dark:disabled:bg-gray-600"
            >
              {isCollecting ? '수집 중...' : '데이터 수집 시작'}
            </button>
          </div>
        </>
      )}

      {progress && (
        <div className="mb-6">
          <CollectionProgressComponent
            progress={progress}
            onCancel={cancelCollection}
          />
        </div>
      )}

      <div>
        <CollectionHistory history={history} />
      </div>
    </div>
  );
}
