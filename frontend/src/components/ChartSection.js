// ChartSection.js
import React, { useMemo } from 'react';
import { Line } from 'react-chartjs-2';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const ChartSection = ({
  loading,
  selectedPrediction,
  hasInsufficientData,
  localEnterpriseData,
  unitBasedData,
  editedData,
  getData,
}) => {
  const chartData = useMemo(() => {
    const labels = MONTHS;
    if (selectedPrediction === 'unit_sold' && unitBasedData) {
      const years = [...new Set(unitBasedData.historical_data.map(item => item.year))].sort().slice(-2);
      const [yearBeforeLast, lastYear] = years;

      return {
        labels,
        datasets: [
          {
            label: `${yearBeforeLast} (Year Before Last)`,
            data: unitBasedData.historical_data.filter(item => item.year === yearBeforeLast).map(item => item.real_income),
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false,
          },
          {
            label: `${lastYear} (Last Year)`,
            data: unitBasedData.historical_data.filter(item => item.year === lastYear).map(item => item.real_income),
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false,
          },
          {
            label: `${unitBasedData.next_year} (Predicted)`,
            data: unitBasedData.next_year_prediction.map(item => item.predicted_income),
            borderColor: 'rgba(54, 162, 235, 1)',
            fill: false,
          }
        ]
      };
    } else {
      const { yearBeforeLast, lastYear, predicted } = getData();
      return {
        labels,
        datasets: [
          {
            label: 'Year Before Last',
            data: yearBeforeLast,
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false,
          },
          {
            label: 'Last Year',
            data: lastYear,
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false,
          },
          {
            label: `${localEnterpriseData?.prediction_year || 'Future'} (Predicted)`,
            data: Object.values(editedData).length > 0 ? Object.values(editedData) : predicted,
            borderColor: 'rgba(54, 162, 235, 1)',
            fill: false,
          },
        ],
      };
    }
  }, [localEnterpriseData, selectedPrediction, editedData, unitBasedData, getData]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (selectedPrediction === 'history' && hasInsufficientData) {
    return (
      <div className="error-message text-red-500 text-center">
        No prediction based on history data, there is no valid data available for the selected enterprise.
      </div>
    );
  }

  return (
    <div className="Chart w-full max-w-2xl p-2">
      <h3 className="text-lg mb-2 text-center">
        {selectedPrediction === 'history'
          ? `Revenue Budget History with Prediction for ${localEnterpriseData?.prediction_year}`
          : `${selectedPrediction.charAt(0).toUpperCase() + selectedPrediction.slice(1)} Based Prediction`}
      </h3>
      <Line data={chartData} />
    </div>
  );
};

export default ChartSection;