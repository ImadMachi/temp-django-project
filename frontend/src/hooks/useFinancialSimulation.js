import { useState } from 'react';
import { saveBulkIncomeDetail } from '../api/enterpriseApi';

const useFinancialSimulation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const saveSimulation = async (simulationData) => {
    setLoading(true);
    setError(null);
    try {
      const result = await saveBulkIncomeDetail(simulationData);
      setLoading(false);
      return result;
    } catch (err) {
      setError(err.message || 'An error occurred while saving the simulation');
      setLoading(false);
      throw err;
    }
  };

  return { saveSimulation, loading, error };
};

export default useFinancialSimulation;