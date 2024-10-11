// ApprovedPredictions.js
import React, { useState, useEffect } from 'react';

const ApprovedPredictions = () => {
  const [approvedPredictions, setApprovedPredictions] = useState([]);

  useEffect(() => {
    const storedPredictions = localStorage.getItem('approvedPredictions');
    if (storedPredictions) {
      setApprovedPredictions(JSON.parse(storedPredictions));
    }
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">Approved Predictions</h1>
      {approvedPredictions.length === 0 ? (
        <p className="text-center text-gray-600">No approved predictions yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {approvedPredictions.map((prediction, index) => (
            <div key={index} className="bg-white shadow-lg rounded-lg overflow-hidden">
              <div className="bg-blue-600 text-white px-4 py-2">
                <h2 className="text-xl font-semibold">{prediction.enterpriseName}</h2>
                <p className="text-sm">ID: {prediction.enterpriseId}</p>
              </div>
              <div className="p-4">
                <p className="text-gray-600 mb-2">
                  <span className="font-semibold">Targeted Revenue:</span> {prediction.targetedRevenue.toLocaleString()}
                </p>
                <p className="text-gray-600 mb-2">
                  <span className="font-semibold">Growth Rate:</span> {(prediction.growthRate * 100).toFixed(2)}%
                </p>
                <p className="text-gray-600 mb-4">
                  <span className="font-semibold">Prediction Type:</span> {prediction.predictionType}
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="px-2 py-1 text-left">Month</th>
                        <th className="px-2 py-1 text-right">Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {prediction.predictionData.map((data, dataIndex) => (
                        <tr key={dataIndex} className={dataIndex % 2 === 0 ? 'bg-gray-50' : ''}>
                          <td className="px-2 py-1">{data.month}</td>
                          <td className="px-2 py-1 text-right">${data.value.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ApprovedPredictions;