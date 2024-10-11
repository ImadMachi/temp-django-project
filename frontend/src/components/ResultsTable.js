import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ChartSection from './ChartSection';
import PredictionButtons from './PredictionButtons';
import DataTable from './DataTable';
import { useResultsData } from '../hooks/useResultsData';
import { usePrediction } from '../hooks/usePrediction';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const ResultsTable = ({ enterpriseData, setEnterpriseData, targetedRevenue, growthRate, revenueId }) => {
  const [approvedPredictions, setApprovedPredictions] = useState([]);
  const navigate = useNavigate();

  const {
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
    hasInsufficientData,
    canDisplayResults,
    getData,
    handleCellEdit,
    fetchHistoryBasedPrediction,
  } = useResultsData(enterpriseData, setEnterpriseData, targetedRevenue, growthRate);

  const { handlePredictionChange } = usePrediction(
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
  );

  useEffect(() => {
    const storedPredictions = localStorage.getItem('approvedPredictions');
    if (storedPredictions) {
      setApprovedPredictions(JSON.parse(storedPredictions));
    }
  }, []);

  // New useEffect to clear local storage when enterprise changes
  useEffect(() => {
    localStorage.removeItem('approvedPredictions');
    setApprovedPredictions([]);
  }, [enterpriseData.id]); // Assuming enterpriseData has an 'id' field

  const handleApprove = () => {
    let tableData;
    if (selectedPrediction === 'unit_sold' && unitBasedData) {
      const years = [...new Set(unitBasedData.historical_data.map(item => item.year))].sort().slice(-2);
      const [yearBeforeLast, lastYear] = years;

      tableData = MONTHS.map((month, index) => {
        const monthIndex = index + 1;
        const yearBeforeLastData = unitBasedData.historical_data.find(item => item.year === yearBeforeLast && item.month === monthIndex);
        const lastYearData = unitBasedData.historical_data.find(item => item.year === lastYear && item.month === monthIndex);
        const predictedData = unitBasedData.next_year_prediction[index];

        return {
          month,
          yearBeforeLast: yearBeforeLastData?.real_income ?? 'N/A',
          lastYear: lastYearData?.real_income ?? 'N/A',
          predicted: predictedData?.predicted_income ?? 'N/A',
          edited: editedData[index] !== undefined ? editedData[index] : predictedData?.predicted_income ?? 'N/A',
        };
      });
    } else {
      const { yearBeforeLast, lastYear, predicted } = getData();
      tableData = MONTHS.map((month, index) => ({
        month,
        yearBeforeLast: yearBeforeLast[index],
        lastYear: lastYear[index],
        predicted: predicted[index],
        edited: editedData[index] !== undefined ? editedData[index] : predicted[index],
      }));
    }

    const newApprovedPrediction = {
      companyName: localEnterpriseData.company_name || enterpriseData.company_name,
      enterpriseName: localEnterpriseData.enterprise_name || enterpriseData.name || enterpriseData.enterprise_name,
      enterpriseId: localEnterpriseData.enterprise_id || enterpriseData.id || enterpriseData.enterprise_id,
      targetedRevenue: targetedRevenue,
      revenueId: revenueId,
      growthRate: growthRate,
      predictionType: selectedPrediction,
      predictionYear: selectedPrediction === 'unit_sold' && unitBasedData ? unitBasedData.next_year : localEnterpriseData?.prediction_year || 'Future',
      tableData: tableData
    };

    const existingPredictionIndex = approvedPredictions.findIndex(
      prediction => prediction.enterpriseId === newApprovedPrediction.enterpriseId &&
        prediction.targetedRevenue === newApprovedPrediction.targetedRevenue &&
        prediction.predictionType === newApprovedPrediction.predictionType &&
        prediction.revenueId === newApprovedPrediction.revenueId
    );

    let updatedPredictions;
    if (existingPredictionIndex !== -1) {
      updatedPredictions = [...approvedPredictions];
      updatedPredictions[existingPredictionIndex] = newApprovedPrediction;
      alert('Existing prediction updated.');
    } else {
      updatedPredictions = [...approvedPredictions, newApprovedPrediction];
      alert('New prediction approved and saved locally.');
    }

    setApprovedPredictions(updatedPredictions);
    localStorage.setItem('approvedPredictions', JSON.stringify(updatedPredictions));
  };

  const handleApproveAll = () => {
    const approvedPredictions = JSON.parse(localStorage.getItem('approvedPredictions') || '[]');
    if (approvedPredictions.length > 0) {
      const enterpriseId = approvedPredictions[0].enterpriseId;
      navigate('/financialtable', { state: { enterpriseId } });
    } else {
      alert('No approved predictions found.');
    }
  };

  const buttonClass = (type) => `
  px-4 py-2 rounded mr-2 mb-2 
  ${selectedPrediction === type ? 'bg-blue-700 text-white' : 'bg-blue-500 text-white'} 
  hover:bg-blue-600 transition-colors duration-300 ease-in-out
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
  shadow-sm font-medium text-sm
  ${!canDisplayResults ? 'opacity-50 cursor-not-allowed' : ''}
`;
  const globalePredictionButtonClass = `
    px-4 py-2 rounded mb-2 
    bg-green-300 text-black
    hover:bg-green-400 transition-colors duration-300 ease-in-out
    focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50
    shadow-sm font-medium text-sm
  `;


  return (
    <div className="ResultsTable border p-4 mb-4">
      <h2 className="text-xl mb-4 text-center">Financial Forecast Results</h2>

      {!canDisplayResults ? (
        <div className="text-center text-gray-600 my-8">
          Please select an enterprise, set a target revenue, and specify a growth rate to view results.
        </div>
      ) : (
        <>
          <div className="ChartContainer flex justify-center mb-6">
            <ChartSection
              loading={loading}
              selectedPrediction={selectedPrediction}
              hasInsufficientData={hasInsufficientData}
              localEnterpriseData={localEnterpriseData}
              unitBasedData={unitBasedData}
              editedData={editedData}
              getData={getData}
            />
          </div>

          <PredictionButtons
            selectedPrediction={selectedPrediction}
            handlePredictionChange={handlePredictionChange}
            canDisplayResults={canDisplayResults}
            buttonClass={buttonClass}
          />

          {error && <p className="text-center text-red-500">Error loading prediction: {error.message}</p>}

          <DataTable
            selectedPrediction={selectedPrediction}
            localEnterpriseData={localEnterpriseData}
            unitBasedData={unitBasedData}
            editedData={editedData}
            handleCellEdit={handleCellEdit}
            getData={getData}
          />

          <div className="flex justify-between items-center mt-4">
            <div className="w-1/3"></div>
            <div className="w-1/3 flex justify-center">
              <button
                className={buttonClass('approve')}
                disabled={!canDisplayResults}
                onClick={handleApprove}
              >
                Approve Budget
              </button>
            </div>
            <div className="w-1/3 flex justify-end">
              <button
                className={globalePredictionButtonClass}
                onClick={handleApproveAll}
              >
                Globale prediction
              </button>
            </div>
          </div>

        </>
      )}
    </div>
  );
};

export default ResultsTable;