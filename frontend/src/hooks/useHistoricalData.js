import { useState, useEffect } from 'react';
import { fetchHistoricalData } from '../api/enterpriseApi';

export const useHistoricalData = (selectedEnterpriseId, selectedDescription) => {
  const [historicalData, setHistoricalData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadHistoricalData = async () => {
      if (!selectedEnterpriseId) return;

      setLoading(true);
      try {
        const data = await fetchHistoricalData(selectedEnterpriseId, selectedDescription);
        console.log("Fetched historical data:", data);
        setHistoricalData(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch historical data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadHistoricalData();
  }, [selectedEnterpriseId, selectedDescription]);

  return { historicalData, loading, error };
};