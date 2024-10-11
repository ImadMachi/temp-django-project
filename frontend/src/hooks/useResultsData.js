// hooks/useResultsData.js
import { useState, useEffect, useMemo, useCallback } from "react";
import { useFetchHistoryBasedPrediction } from "./useFetchHistoryBasedPrediction";

export const useResultsData = (
  enterpriseData,
  setEnterpriseData,
  targetedRevenue,
  growthRate
) => {
  const [selectedPrediction, setSelectedPrediction] = useState("history");
  const [editedData, setEditedData] = useState({});
  const [unitBasedData, setUnitBasedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [localEnterpriseData, setLocalEnterpriseData] =
    useState(enterpriseData);

  const fetchHistoryBasedPrediction = useFetchHistoryBasedPrediction(
    localEnterpriseData,
    growthRate,
    targetedRevenue,
    setEnterpriseData,
    setLocalEnterpriseData,
    setLoading,
    setError
  );

  const hasInsufficientData = useMemo(() => {
    return (
      !localEnterpriseData?.results ||
      Object.keys(localEnterpriseData.results).length === 0
    );
  }, [localEnterpriseData]);

  const canDisplayResults = useMemo(() => {
    return (
      localEnterpriseData &&
      targetedRevenue &&
      localEnterpriseData.enterprise_id &&
      growthRate !== undefined
    );
  }, [localEnterpriseData, targetedRevenue, growthRate]);

  useEffect(() => {
    if (
      localEnterpriseData.enterprise_id !== enterpriseData.enterprise_id ||
      localEnterpriseData.targetedRevenue !== targetedRevenue ||
      localEnterpriseData.growthRate !== growthRate
    ) {
      console.log("--------------", localEnterpriseData);
      setLocalEnterpriseData({
        ...enterpriseData,
        targetedRevenue,
        growthRate,
      });
      setEditedData({});
      setUnitBasedData(null);
      setError(null);
      setSelectedPrediction("history");
    }
  }, [enterpriseData, targetedRevenue, growthRate]);

  const generateDummyData = useCallback(
    () =>
      Array(12)
        .fill(0)
        .map(() => Math.floor(Math.random() * 10000) + 1000),
    []
  );

  const getData = useCallback(() => {
    if (
      selectedPrediction === "history" &&
      !hasInsufficientData &&
      localEnterpriseData.results
    ) {
      const description = Object.keys(localEnterpriseData.results)[0];
      const data = localEnterpriseData.results[description];
      const predictionYear = localEnterpriseData.prediction_year;
      return {
        yearBeforeLast: Object.values(data[predictionYear - 2] || {}),
        lastYear: Object.values(data[predictionYear - 1] || {}),
        predicted: Object.values(data[predictionYear] || {}),
      };
    }
    const dummyData = generateDummyData();
    return {
      yearBeforeLast: dummyData,
      lastYear: dummyData,
      predicted: dummyData,
    };
  }, [
    selectedPrediction,
    hasInsufficientData,
    localEnterpriseData,
    generateDummyData,
  ]);

  const handleCellEdit = useCallback((rowIndex, value) => {
    setEditedData((prev) => ({
      ...prev,
      [rowIndex]: parseFloat(value) || 0,
    }));
  }, []);

  useEffect(() => {
    if (canDisplayResults) {
      fetchHistoryBasedPrediction();
    }
  }, [canDisplayResults, fetchHistoryBasedPrediction]);

  return {
    selectedPrediction,
    setSelectedPrediction,
    editedData,
    setEditedData,
    unitBasedData,
    setUnitBasedData,
    loading,
    setLoading,
    error,
    setError,
    localEnterpriseData,
    setLocalEnterpriseData,
    hasInsufficientData,
    canDisplayResults,
    getData,
    handleCellEdit,
    fetchHistoryBasedPrediction,
  };
};
