import { useState, useEffect } from 'react';
import { fetchEnterprises } from '../api/enterpriseApi';

export const useEnterprises = () => {
  const [enterprises, setEnterprises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadEnterprises = async () => {
      try {
        const data = await fetchEnterprises();
        const simplifiedEnterprises = data.map(enterprise => ({
          enterprise_id: enterprise.enterprise_id,
          enterprise_name: enterprise.enterprise_name,
          start_period: enterprise.start_period
        }));
        setEnterprises(simplifiedEnterprises);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch enterprises');
        setLoading(false);
      }
    };

    loadEnterprises();
  }, []);

  return { enterprises, loading, error };
};