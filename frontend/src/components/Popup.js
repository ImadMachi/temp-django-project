import React, { useState, useEffect } from 'react';
import Button from '../Button';
import '../Popup.css';
import Configuration from './Configuration';
import Charts from './Charts';
import ResultsTable from './ResultsTable';
import Options from "./Option";
import { fetchEnterpriseData } from '../api/enterpriseApi';

const Popup = () => {
  const [config, setConfig] = useState({
    recurrentRevenue: false,
    includeHypothesis: false,
    includeOtherCompanies: false,
    salesBudgetHistory: false,
    orderBooksHistory: false,
    opportunityHistory: false,
    budgetHistory: false,
    realHistory: false,
    performanceHistory: false,
  });
  const [validationData, setValidationData] = useState(null);
  const [selectedEnterpriseId, setSelectedEnterpriseId] = useState(null);
  const [enterpriseData, setEnterpriseData] = useState(null);
  const [selectedYear, setSelectedYear] = useState('2025');
  const [statementType, setStatementType] = useState('revenue');
  const [targetedRevenue, setTargetedRevenue] = useState('');
  const [revenueId, setRevenueId] = useState('');

  const [accountId, setAccountId] = useState('');
  const [growthRate, setGrowthRate] = useState(0.05);
  const [startedMonth, setStartedMonth] = useState('');

  useEffect(() => {
    if (validationData && validationData.validations) {
      setConfig(prevConfig => ({
        ...prevConfig,
        recurrentRevenue: validationData.validations.recurrent_revenue || false,
        salesBudgetHistory: validationData.validations.monthly_sales_budget || false,
        orderBooksHistory: validationData.validations.monthly_order_book || false,
        opportunityHistory: validationData.validations.monthly_opportunity || false,
        budgetHistory: validationData.validations.sales_budget || false,
        realHistory: validationData.validations.monthly_revenue || false,
        performanceHistory: validationData.validations.monthly_performance || false,
        includeOtherCompanies: prevConfig.includeOtherCompanies,
        includeHypothesis: prevConfig.includeHypothesis,
      }));
    }
  }, [validationData]);

  const handleConfigChange = (key) => {
    setConfig(prevConfig => {
      const newConfig = {
        ...prevConfig,
        [key]: !prevConfig[key],
      };
      console.log('New config:', newConfig);
      return newConfig;
    });
  };

  const handleEnterpriseSelect = async (data, enterpriseId) => {
    setValidationData(data);
    console.log('Data', data);
    setSelectedEnterpriseId(enterpriseId);
    console.log("Selected Enterprise ID:", enterpriseId);

    try {
      const fetchedEnterpriseData = await fetchEnterpriseData(enterpriseId);
      console.log("Fetched Enterprise Data:", fetchedEnterpriseData);
      setEnterpriseData(fetchedEnterpriseData);
    } catch (error) {
      console.error('Error fetching enterprise data:', error);
    }
  };

  const handleYearChange = (year) => {
    setSelectedYear(year);
  };

  const handleStatementTypeChange = (type) => {
    setStatementType(type);
  };

  const handleTargetedRevenueChange = (revenue) => {
    setTargetedRevenue(revenue);
  };
  const handleTargetedRevenueIdChange = (revenue_id) => {
    setRevenueId(revenue_id);
  };
  const handleAccountIdChange = (id) => {
    setAccountId(id);
  };

  const handleGrowthRateChange = (rate) => {
    const parsedRate = parseFloat(rate);
    if (!isNaN(parsedRate)) {
      setGrowthRate(parsedRate);
      console.log("Growth rate updated:", parsedRate);
    }
  };

  const handleStartedMonthChange = (month) => {
    setStartedMonth(month);
  };

  return (
    <div className="App bg-white">
      <header className="App-header">
        <h1 style={{ fontSize: '20px', marginBottom: '12px', color: '#1f2937', fontWeight: '600' }}>Revenues Budgets Simulation</h1>
      </header>
      <div className="Content">
        {enterpriseData && enterpriseData.name && (
          <h2 className="text-lg font-semibold mb-4">Selected Enterprise: {enterpriseData.name}</h2>
        )}
        <Options
          onEnterpriseSelect={handleEnterpriseSelect}
          onYearChange={handleYearChange}
          onStatementTypeChange={handleStatementTypeChange}
          onTargetedRevenueChange={handleTargetedRevenueChange}
          onTargetedRevenueIdChange={handleTargetedRevenueIdChange}
          onAccountIdChange={handleAccountIdChange}
          onStartedMonthChange={handleStartedMonthChange}
          selectedYear={selectedYear}
          statementType={statementType}
          targetedRevenue={targetedRevenue}
          revenueId={revenueId}
          accountId={accountId}
          startedMonth={startedMonth}
        />
        <Configuration
          config={config}
          onConfigChange={handleConfigChange}
          validationData={validationData}
          onGrowthRateChange={handleGrowthRateChange}
        />
        <Button />
        <Charts
          config={config}
          selectedEnterpriseId={selectedEnterpriseId}
          selectedYear={selectedYear}
          statementType={statementType}
          targetedRevenue={targetedRevenue}
        />
        {enterpriseData && (
          <ResultsTable
            key={selectedEnterpriseId}
            enterpriseData={enterpriseData}
            setEnterpriseData={setEnterpriseData}
            selectedYear={selectedYear}
            statementType={statementType}
            targetedRevenue={targetedRevenue}
            revenueId={revenueId}
            accountId={accountId}
            growthRate={growthRate}
          />
        )}
      </div>
    </div>
  );
}

export default Popup;
