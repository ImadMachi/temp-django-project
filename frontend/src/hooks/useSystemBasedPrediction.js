import { useState, useEffect } from 'react';
import { getSystemBasedPrediction } from '../api/enterpriseApi';

export const useSystemBasedPrediction = (enterpriseId, description, growthRate, trigger) => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrediction = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await getSystemBasedPrediction(enterpriseId, description, growthRate);
        setPrediction(result);
      } catch (err) {
        setError(err.message || 'An error occurred while fetching the prediction.');
      } finally {
        setLoading(false);
      }
    };

    if (enterpriseId && description && growthRate && trigger) {
      fetchPrediction();
    }
  }, [enterpriseId, description, growthRate, trigger]);

  return { prediction, loading, error };
};