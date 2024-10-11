import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import { Chart as ChartJS, TimeScale, CategoryScale } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { useHistoricalData } from '../hooks/useHistoricalData';
import { fetchAggregatedData } from '../api/enterpriseApi';

ChartJS.register(TimeScale, CategoryScale);

function Charts({ config = {}, selectedEnterpriseId, targetedRevenue }) {
  const { historicalData, loading, error } = useHistoricalData(selectedEnterpriseId, targetedRevenue);
  const [chartData, setChartData] = useState({});
  const [aggregatedData, setAggregatedData] = useState(null);
  const [isLoading, setIsLoading] = useState({});

  useEffect(() => {
    console.log('Config changed:', config);
    console.log('Selected Enterprise ID:', selectedEnterpriseId);
    console.log('Targeted Revenue:', targetedRevenue);

    if (config.includeOtherCompanies && selectedEnterpriseId && targetedRevenue) {
      console.log('Fetching aggregated data...');
      setIsLoading(prev => ({ ...prev, aggregated: true }));
      fetchAggregatedData(selectedEnterpriseId, targetedRevenue)
        .then(data => {
          console.log('Fetched aggregated data:', data);
          setAggregatedData(data);
          setIsLoading(prev => ({ ...prev, aggregated: false }));
        })
        .catch(err => {
          console.error('Error fetching aggregated data:', err);
          setIsLoading(prev => ({ ...prev, aggregated: false }));
        });
    }
  }, [config.includeOtherCompanies, selectedEnterpriseId, targetedRevenue]);

  useEffect(() => {
    if (!selectedEnterpriseId || !targetedRevenue) return;

    console.log('Updating chart data...');
    console.log('Historical Data:', historicalData);
    console.log('Aggregated Data:', aggregatedData);

    const newChartData = {};
    const newIsLoading = {};

    if (historicalData && historicalData.historical_data) {
      Object.keys(config).forEach(key => {
        if (config[key]) {
          const dataKey = getDataKey(key);
          if (dataKey) {
            newIsLoading[key] = true;
            setIsLoading(prev => ({ ...prev, [key]: true }));
            newChartData[key] = generateChartData(dataKey, historicalData.historical_data);
            console.log(`Generated chart data for ${key}:`, newChartData[key]);
            newIsLoading[key] = false;
          }
        }
      });
    }

    if (config.includeOtherCompanies && aggregatedData && aggregatedData.aggregated_data) {
      console.log('Processing aggregated data...');
      if (aggregatedData.aggregated_data.aggregatedAverageReals) {
        newIsLoading['aggregatedAverageReals'] = true;
        setIsLoading(prev => ({ ...prev, aggregatedAverageReals: true }));
        newChartData['aggregatedAverageReals'] = generateAggregatedChartData(aggregatedData.aggregated_data.aggregatedAverageReals);
        console.log('Generated aggregatedAverageReals chart data:', newChartData['aggregatedAverageReals']);
        newIsLoading['aggregatedAverageReals'] = false;
      }
      if (aggregatedData.aggregated_data.aggregatedAverageBudgets) {
        newIsLoading['aggregatedAverageBudgets'] = true;
        setIsLoading(prev => ({ ...prev, aggregatedAverageBudgets: true }));
        newChartData['aggregatedAverageBudgets'] = generateAggregatedChartData(aggregatedData.aggregated_data.aggregatedAverageBudgets);
        console.log('Generated aggregatedAverageBudgets chart data:', newChartData['aggregatedAverageBudgets']);
        newIsLoading['aggregatedAverageBudgets'] = false;
      }
    }

    console.log('New Chart Data:', newChartData);
    setChartData(newChartData);
    setIsLoading(newIsLoading);
  }, [config, historicalData, aggregatedData, selectedEnterpriseId, targetedRevenue]);

  const getDataKey = (configKey) => {
    switch (configKey) {
      case 'salesBudgetHistory': return 'Sales Budget history';
      case 'performanceHistory': return 'Revenues Performance History';
      case 'realHistory': return 'Revenues Real History';
      default: return '';
    }
  };

  const generateChartData = (dataKey, data) => {
    if (!data || !data[dataKey]) return null;

    const chartData = data[dataKey];
    const years = [...new Set(chartData.map(item => item.year))];

    const datasets = years.map((year, index) => {
      const yearData = chartData.filter(item => item.year === year && item.description === targetedRevenue);
      let dataField;
      switch (dataKey) {
        case 'Revenues Performance History':
          dataField = 'performance';
          break;
        case 'Revenues Real History':
          dataField = 'real';
          break;
        case 'Sales Budget history':
          dataField = 'budget';
          break;
        default:
          dataField = 'value';
      }

      return {
        label: year,
        data: yearData.map(item => ({
          x: item.month - 1,
          y: item[dataField]
        })),
        borderColor: `hsl(${index * 360 / years.length}, 70%, 50%)`,
        fill: false,
      };
    });

    return {
      datasets: datasets,
    };
  };

  const generateAggregatedChartData = (data) => {
    if (!data) return null;
    console.log('Generating aggregated chart data for:', data);
    const years = Object.keys(data);
    const datasets = years.map((year, index) => ({
      label: year,
      data: data[year].map(item => ({
        x: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].indexOf(item.month),
        y: item.value
      })),
      borderColor: `hsl(${index * 360 / years.length}, 70%, 50%)`,
      fill: false,
    }));

    return { datasets };
  };

  const chartConfigs = [
    { key: 'salesBudgetHistory', title: 'Sales Budget History' },
    { key: 'performanceHistory', title: 'Revenues Performance History' },
    { key: 'realHistory', title: 'Revenues Real History' },
  ];

  // Only add aggregated charts if their data is available
  if (chartData['aggregatedAverageReals']) {
    chartConfigs.push({ key: 'aggregatedAverageReals', title: 'Aggregated Average Reals' });
  }
  if (chartData['aggregatedAverageBudgets']) {
    chartConfigs.push({ key: 'aggregatedAverageBudgets', title: 'Aggregated Average Budgets' });
  }

  if (!selectedEnterpriseId || !targetedRevenue) {
    return null;
  }

  if (loading) {
    return (
      <div className="Charts border p-4 mb-4 flex flex-col items-center justify-center min-h-[400px]">
        <h2 className="text-xl mb-8 text-center">Charts</h2>
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) return <div>Error loading chart data: {error}</div>;

  return (
    <div className="Charts border p-4 mb-4">
      <h2 className="text-xl mb-4 text-center">Charts</h2>
      <div className="flex flex-wrap justify-between">
        {chartConfigs.map(({ key, title }) => (
          <div key={key} className="Chart w-full md:w-1/2 p-2">
            <h3 className="text-lg mb-2 text-center">{title}</h3>
            {isLoading[key] ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
              </div>
            ) : chartData[key] ? (
              <Line
                data={chartData[key]}
                options={{
                  responsive: true,
                  scales: {
                    x: {
                      type: 'category',
                      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                      title: {
                        display: true,
                        text: 'Month'
                      }
                    },
                    y: {
                      beginAtZero: true,
                      title: {
                        display: true,
                        text: 'Value'
                      }
                    }
                  },
                  plugins: {
                    legend: {
                      position: 'top',
                    },
                    title: {
                      display: true,
                      text: `${title} - ${targetedRevenue}`
                    }
                  }
                }}
              />
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Charts;