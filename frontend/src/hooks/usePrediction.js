// hooks/usePrediction.js
import { useCallback } from 'react';
import { fetchUnitBasedRevenuePrediction } from '../api/enterpriseApi';

export const usePrediction = (
  canDisplayResults,
  setSelectedPrediction,
  setEditedData,
  setUnitBasedData,
  localEnterpriseData,
  growthRate,
  targetedRevenue,
  setLoading,
  setError,
  fetchHistoryBasedPrediction
) => {
  const handlePredictionChange = useCallback(async (type) => {
    if (!canDisplayResults) return;

    setSelectedPrediction(type);
    setEditedData({});
    setLoading(true);

    try {
      if (type === 'unit_sold') {
        console.log("Fetching with growth rate:", growthRate, "and targetedRevenue:", targetedRevenue);
        const data = await fetchUnitBasedRevenuePrediction(localEnterpriseData.enterprise_id, growthRate, targetedRevenue);
        setUnitBasedData(data);
      } else if (type === 'history') {
        await fetchHistoryBasedPrediction();
      }
      setError(null);
    } catch (err) {
      console.error('Error fetching prediction:', err);
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [canDisplayResults, setSelectedPrediction, setEditedData, setUnitBasedData, localEnterpriseData, growthRate, targetedRevenue, setLoading, setError, fetchHistoryBasedPrediction]);

  return { handlePredictionChange };
};