
import { useState, useEffect } from 'react';
import { fetchRevenueDescriptions } from '../api/enterpriseApi';

export const useRevenueDescriptions = (enterpriseId) => {
  const [descriptions, setDescriptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDescriptions = async () => {
      if (!enterpriseId) {
        setDescriptions([]);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const data = await fetchRevenueDescriptions(enterpriseId);
        setDescriptions(data);
      } catch (err) {
        setError('Error fetching revenue descriptions');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDescriptions();
  }, [enterpriseId]);

  console.log(descriptions)
  return { descriptions, loading, error };
};