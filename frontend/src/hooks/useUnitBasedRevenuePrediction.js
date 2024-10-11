import { useState, useEffect } from 'react';
import { fetchUnitBasedRevenuePrediction } from '../api/enterpriseApi';

export const useUnitBasedRevenuePrediction = (enterpriseId, growthRate, description) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!enterpriseId || growthRate === undefined || !description) {
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        const result = await fetchUnitBasedRevenuePrediction(enterpriseId, growthRate, description);
        setData(result);
        setError(null);
      } catch (error) {
        console.error('Error fetching unit-based revenue prediction:', error);
        setError(error);
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [enterpriseId, growthRate, description]);

  return { data, loading, error };
};