import { useState, useCallback, useRef } from 'react';
import {
  CollectionConfig,
  CollectionProgress,
  ApiProgress,
  CollectionHistoryItem,
} from '@/types/batch-collection';
import {
  getMockCollectionHistory,
  saveMockCollectionHistory,
  getRegionName,
  getApiName,
  API_OPTIONS,
} from '@/lib/batch-collection-mock';

export function useBatchCollection() {
  const [isCollecting, setIsCollecting] = useState(false);
  const [progress, setProgress] = useState<CollectionProgress | null>(null);
  const cancelledRef = useRef(false);

  const generateMonths = useCallback((startMonth: string, endMonth: string): string[] => {
    const months: string[] = [];
    const start = parseInt(startMonth);
    const end = parseInt(endMonth);
    const startYear = Math.floor(start / 100);
    const startMon = start % 100;
    const endYear = Math.floor(end / 100);
    const endMon = end % 100;

    for (let year = startYear; year <= endYear; year++) {
      const monthStart = year === startYear ? startMon : 1;
      const monthEnd = year === endYear ? endMon : 12;
      for (let month = monthStart; month <= monthEnd; month++) {
        months.push(`${year}${month.toString().padStart(2, '0')}`);
      }
    }
    return months;
  }, []);

  const startCollection = useCallback(
    async (config: CollectionConfig): Promise<void> => {
      cancelledRef.current = false;
      setIsCollecting(true);

      const collectionId = `col_${Date.now()}`;
      const months = generateMonths(config.startMonth, config.endMonth);
      const totalTasks = config.regions.length * config.apis.length * months.length;

      const initialProgress: CollectionProgress = {
        id: collectionId,
        status: 'running',
        config,
        overallProgress: 0,
        apiProgress: config.apis.map((apiId) => ({
          apiId,
          apiName: getApiName(apiId),
          status: 'pending',
          current: 0,
          total: config.regions.length * months.length,
          successCount: 0,
          errorCount: 0,
        })),
        startTime: new Date().toISOString(),
        totalRecords: 0,
      };

      setProgress(initialProgress);

      let completedTasks = 0;
      let totalRecords = 0;

      for (let apiIndex = 0; apiIndex < config.apis.length; apiIndex++) {
        if (cancelledRef.current) {
          break;
        }

        const apiId = config.apis[apiIndex];
        const apiProgress = initialProgress.apiProgress[apiIndex];

        setProgress((prev) => {
          if (!prev) return prev;
          const updatedApiProgress = [...prev.apiProgress];
          updatedApiProgress[apiIndex] = { ...apiProgress, status: 'running' };
          return { ...prev, apiProgress: updatedApiProgress };
        });

        for (let regionIndex = 0; regionIndex < config.regions.length; regionIndex++) {
          if (cancelledRef.current) {
            break;
          }

          const regionCode = config.regions[regionIndex];

          for (let monthIndex = 0; monthIndex < months.length; monthIndex++) {
            if (cancelledRef.current) {
              break;
            }

            const month = months[monthIndex];

            setProgress((prev) => {
              if (!prev) return prev;
              const updatedApiProgress = [...prev.apiProgress];
              updatedApiProgress[apiIndex] = {
                ...updatedApiProgress[apiIndex],
                current: regionIndex * months.length + monthIndex + 1,
                currentMonth: month,
              };
              return { ...prev, apiProgress: updatedApiProgress };
            });

            await new Promise((resolve) => setTimeout(resolve, 100));

            const success = Math.random() > 0.05;
            const recordCount = success ? Math.floor(Math.random() * 500) + 50 : 0;

            if (success) {
              totalRecords += recordCount;
            }

            completedTasks++;

            setProgress((prev) => {
              if (!prev) return prev;
              const updatedApiProgress = [...prev.apiProgress];
              updatedApiProgress[apiIndex] = {
                ...updatedApiProgress[apiIndex],
                successCount: success
                  ? updatedApiProgress[apiIndex].successCount + 1
                  : updatedApiProgress[apiIndex].successCount,
                errorCount: success
                  ? updatedApiProgress[apiIndex].errorCount
                  : updatedApiProgress[apiIndex].errorCount + 1,
              };

              const overallProgress = completedTasks / totalTasks;
              const estimatedTimeRemaining = (totalTasks - completedTasks) * 100;
              const estimatedEndTime = new Date(Date.now() + estimatedTimeRemaining).toISOString();

              return {
                ...prev,
                apiProgress: updatedApiProgress,
                overallProgress,
                totalRecords,
                estimatedEndTime,
              };
            });
          }
        }

        setProgress((prev) => {
          if (!prev) return prev;
          const updatedApiProgress = [...prev.apiProgress];
          updatedApiProgress[apiIndex] = {
            ...updatedApiProgress[apiIndex],
            status: 'completed',
          };
          return { ...prev, apiProgress: updatedApiProgress };
        });
      }

      const finalStatus = cancelledRef.current ? 'cancelled' : 'completed';
      const endTime = new Date().toISOString();

      setProgress((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          status: finalStatus,
          endTime,
          overallProgress: cancelledRef.current ? prev.overallProgress : 1,
        };
      });

      const historyItem: CollectionHistoryItem = {
        id: collectionId,
        startTime: initialProgress.startTime,
        endTime,
        config,
        status: finalStatus as 'completed' | 'error' | 'cancelled',
        totalRecords,
        successCount: initialProgress.apiProgress.reduce(
          (sum, api) => sum + api.successCount,
          0
        ),
        errorCount: initialProgress.apiProgress.reduce((sum, api) => sum + api.errorCount, 0),
        regionNames: config.regions.map((code) => getRegionName(code)),
        apiNames: config.apis.map((apiId) => getApiName(apiId)),
      };

      const history = getMockCollectionHistory();
      const updatedHistory = [historyItem, ...history];
      saveMockCollectionHistory(updatedHistory);

      setIsCollecting(false);
    },
    [generateMonths]
  );

  const cancelCollection = useCallback(() => {
    cancelledRef.current = true;
    setProgress((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        status: 'cancelled',
        endTime: new Date().toISOString(),
      };
    });
    setIsCollecting(false);
  }, []);

  const getCollectionHistory = useCallback((): CollectionHistoryItem[] => {
    return getMockCollectionHistory();
  }, []);

  return {
    isCollecting,
    progress,
    startCollection,
    cancelCollection,
    getCollectionHistory,
  };
}
