// hooks/useChartData.js
import { useMemo } from 'react';
import { MONTHS } from '../constants';

export const useChartData = (selectedPrediction, localEnterpriseData, unitBasedData, editedData) => {
  return useMemo(() => {
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
      const getData = () => {
        if (selectedPrediction === 'history' && localEnterpriseData.results) {
          const description = Object.keys(localEnterpriseData.results)[0];
          const data = localEnterpriseData.results[description];
          const predictionYear = localEnterpriseData.prediction_year;
          return {
            yearBeforeLast: Object.values(data[predictionYear - 2] || {}),
            lastYear: Object.values(data[predictionYear - 1] || {}),
            predicted: Object.values(data[predictionYear] || {}),
          };
        }
        const generateDummyData = () => Array(12).fill(0).map(() => Math.floor(Math.random() * 10000) + 1000);
        const dummyData = generateDummyData();
        return { yearBeforeLast: dummyData, lastYear: dummyData, predicted: dummyData };
      };

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
  }, [selectedPrediction, localEnterpriseData, unitBasedData, editedData]);
};