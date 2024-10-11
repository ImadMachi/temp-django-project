import { useState, useEffect } from 'react';
import { fetchLatestOpportunityBook } from '../api/enterpriseApi';

const useOpportunityBook = (enterpriseId) => {
  const [opportunityBook, setOpportunityBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOpportunityBook = async () => {
      try {
        setLoading(true);
        const data = await fetchLatestOpportunityBook(enterpriseId);
        setOpportunityBook(data);
        setError(null);
      } catch (err) {
        setError(err.message || 'An error occurred while fetching the opportunity book.');
      } finally {
        setLoading(false);
      }
    };

    if (enterpriseId) {
      fetchOpportunityBook();
    }
  }, [enterpriseId]);

  return { opportunityBook, loading, error };
};

export default useOpportunityBook;