// PredictionButtons.js
import React from 'react';

const PredictionButtons = ({ selectedPrediction, handlePredictionChange, canDisplayResults, buttonClass }) => {
  return (
    <div className="flex flex-wrap justify-center mb-4">
      {['profile', 'history', 'system', 'unit_sold'].map(type => (
        <button
          key={type}
          className={buttonClass(type)}
          onClick={() => handlePredictionChange(type)}
          disabled={!canDisplayResults}
        >
          {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')} Based
        </button>
      ))}
    </div>
  );
};

export default PredictionButtons;