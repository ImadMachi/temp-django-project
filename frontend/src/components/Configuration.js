import React, { useState } from 'react';
import './Configuration.css';


function Configuration({ config, onConfigChange, onGrowthRateChange }) {
  const [localConfig, setLocalConfig] = useState({ growthRate: config.growthRate || '' });
  const checkboxConfig = {
    recurrentRevenue: 'Recurrent Revenue',
    // includeHypothesis: 'Include hypothesis',
    includeOtherCompanies: 'Include other companies with the same product type',
    salesBudgetHistory: 'Include Sales Budget history',
    orderBooksHistory: 'Include order books history',
    opportunityHistory: 'Include opportunity books history',
    // budgetHistory: 'Work with budget history',
    realHistory: 'Work with real history',
    performanceHistory: 'Include performance history'
  };

  const containerStyle = {
    border: '1px solid #e0e0e0',
    borderRadius: '2px',
    padding: '16px',
    marginBottom: '16px',
    backgroundColor: 'white',
  };
  const handleGrowthRateChange = (event) => {
    const value = event.target.value;
    // Allow only numbers
    const regex = /^[0-9]*$/;

    if (regex.test(value)) {
      // Convert the value to a decimal by dividing by 100, if value is not empty
      const decimalValue = value ? (parseFloat(value) / 100).toString() : '';
      setLocalConfig({ ...localConfig, growthRate: decimalValue });
      onGrowthRateChange(decimalValue); // Call the prop function directly with the decimal value
    }
  };

  const handleBlur = () => {
    if (!localConfig.growthRate) {
      // If input is empty, set to default 5%
      setLocalConfig({ ...localConfig, growthRate: '0.05' });
      onGrowthRateChange('0.05');
    }
  };


  return (
    <div style={containerStyle}>
      <h2 style={{ fontSize: '16px', marginBottom: '16px', color: '#333', fontWeight: '600' }}>Configuration</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '16px' }}>
        {Object.entries(checkboxConfig).map(([key, label]) => (
          <label key={key} style={{ display: 'flex', alignItems: 'center', fontSize: '14px', color: '#555' }}>
            <input
              type="checkbox"
              className="custom-checkbox"
              checked={config[key]}
              onChange={() => onConfigChange(key)}
            />
            <span style={{ marginLeft: '8px' }}>{label}</span>
          </label>
        ))}
      </div>
      <div>
        <label style={{ fontSize: '14px', color: '#555', display: 'flex', alignItems: 'center' }}>
          Growth Rate (%):
          <input
            type="text"
            className="growth-rate-input"
            value={localConfig.growthRate ? (parseFloat(localConfig.growthRate) * 100).toString() : ''}
            onChange={handleGrowthRateChange}
            onBlur={handleBlur}  // Add onBlur to handle setting the default
            placeholder="5"  // Updated placeholder to suggest the default value
            pattern="[0-9]*"
          />
        </label>


      </div>
    </div>
  );
}

export default Configuration;