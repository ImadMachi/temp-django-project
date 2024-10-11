import React, { useState } from 'react';
import Configuration from './Configuration';
import ResultsTable from './ResultsTable';

function Dashboard() {
  const [showSalesBudget, setShowSalesBudget] = useState(false);
  const [showRealBudgets, setShowRealBudgets] = useState(false);
  const [showCompanies, setShowCompanies] = useState(false);
  const [showOpportunityHistory, setShowOpportunityHistory] = useState(false);
  const [showPerformanceHistory, setShowPerformanceHistory] = useState(false);
  const [showLostBudget, setShowLostBudget] = useState(false);
  const [showHypothesisIncrease, setShowHypothesisIncrease] = useState(false);

  return (
    <div className="Dashboard">
      <Configuration
        showSalesBudget={showSalesBudget}
        setShowSalesBudget={setShowSalesBudget}
        showRealBudgets={showRealBudgets}
        setShowRealBudgets={setShowRealBudgets}
        showCompanies={showCompanies}
        setShowCompanies={setShowCompanies}
        showOpportunityHistory={showOpportunityHistory}
        setShowOpportunityHistory={setShowOpportunityHistory}
        showPerformanceHistory={showPerformanceHistory}
        setShowPerformanceHistory={setShowPerformanceHistory}
        showLostBudget={showLostBudget}
        setShowLostBudget={setShowLostBudget}
        showHypothesisIncrease={showHypothesisIncrease}
        setShowHypothesisIncrease={setShowHypothesisIncrease}
      />
      <ResultsTable
        showSalesBudget={showSalesBudget}
        showRealBudgets={showRealBudgets}
        showCompanies={showCompanies}
        showOpportunityHistory={showOpportunityHistory}
        showPerformanceHistory={showPerformanceHistory}
        showLostBudget={showLostBudget}
        showHypothesisIncrease={showHypothesisIncrease}
      />
    </div>
  );
}

export default Dashboard;
