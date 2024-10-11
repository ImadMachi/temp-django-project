// hooks/useFetchHistoryBasedPrediction.js
import { useCallback } from 'react';
import { fetchEnterpriseData } from '../api/enterpriseApi';

export const useFetchHistoryBasedPrediction = (
  localEnterpriseData,
  growthRate,
  targetedRevenue,
  setEnterpriseData,
  setLocalEnterpriseData,
  setLoading,
  setError
) => {
  const fetchHistoryBasedPrediction = useCallback(async () => {
    if (!localEnterpriseData.enterprise_id || targetedRevenue === undefined || growthRate === undefined) return;

    setLoading(true);
    try {
      const data = await fetchEnterpriseData(localEnterpriseData.enterprise_id, growthRate, targetedRevenue);
      setEnterpriseData?.(data);
      setLocalEnterpriseData(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching history-based prediction:', err);
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [localEnterpriseData.enterprise_id, targetedRevenue, growthRate, setEnterpriseData, setLocalEnterpriseData, setLoading, setError]);

  return fetchHistoryBasedPrediction;
};