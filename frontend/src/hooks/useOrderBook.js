import { useState, useEffect } from 'react';
import { fetchLatestOrderBook } from '../api/enterpriseApi';

const useOrderBook = (enterpriseId) => {
  const [orderBook, setOrderBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrderBook = async () => {
      try {
        setLoading(true);
        const data = await fetchLatestOrderBook(enterpriseId);
        setOrderBook(data);
        setError(null);
      } catch (err) {
        setError(err.message || 'An error occurred while fetching the order book.');
      } finally {
        setLoading(false);
      }
    };

    if (enterpriseId) {
      fetchOrderBook();
    }
  }, [enterpriseId]);

  return { orderBook, loading, error };
};

export default useOrderBook;