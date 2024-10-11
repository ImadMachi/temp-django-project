import React, { useState, useEffect } from 'react';
import { useEnterprises } from '../hooks/useEnterprises';
import { useRevenueDescriptions } from '../hooks/useRevenueDescriptions';
import { fetchValidationData } from '../api/enterpriseApi';

function Options({
  onEnterpriseSelect,
  onYearChange,
  onStatementTypeChange,
  onTargetedRevenueChange,
  onTargetedRevenueIdChange,
  onStartedMonthChange,
  selectedYear,
  statementType,
  targetedRevenue,
  revenueId,
  startedMonth
}) {
  const { enterprises, loading: enterprisesLoading, error: enterprisesError } = useEnterprises();
  const [selectedEnterprise, setSelectedEnterprise] = useState('');
  const { descriptions, loading: descriptionsLoading, error: descriptionsError } = useRevenueDescriptions(selectedEnterprise);
  const [isSelectionComplete, setIsSelectionComplete] = useState(false);

  useEffect(() => {
    setIsSelectionComplete(selectedEnterprise !== '' && targetedRevenue !== '');
    onYearChange((new Date().getFullYear() + 1).toString());
  }, [selectedEnterprise, targetedRevenue, onYearChange]);

  const handleEnterpriseChange = async (event) => {
    const enterpriseId = event.target.value;
    setSelectedEnterprise(enterpriseId);
    onTargetedRevenueChange('');
    onTargetedRevenueIdChange('');
    if (enterpriseId) {
      try {
        const data = await fetchValidationData(enterpriseId);
        onEnterpriseSelect(data, enterpriseId);

        const selectedEnterpriseData = enterprises.find(e => e.enterprise_id.toString() === enterpriseId);
        if (selectedEnterpriseData) {
          const startMonth = getMonthFromPeriod(selectedEnterpriseData.start_period);
          onStartedMonthChange(startMonth);
        }
      } catch (error) {
        console.error('Error fetching validation data:', error);
      }
    }
  };

  const handleTargetedRevenueChange = (value, id) => {
    onTargetedRevenueChange(value);
    onTargetedRevenueIdChange(id);
    console.log("Selected revenue:", value);
    console.log("Selected revenue ID:", id);
  };

  const getMonthFromPeriod = (period) => {
    const months = [
      'january', 'february', 'march', 'april', 'may', 'june',
      'july', 'august', 'september', 'october', 'november', 'december'
    ];
    return months[period - 1] || '';
  };

  const nextYear = new Date().getFullYear() + 1;

  return (
    <div className="Options border p-4 mb-4">
      <h2 className="text-xl mb-4 text-black">Options</h2>
      <form className="space-y-4">
        <div className="flex items-center space-x-4">
          <label className="block flex-1 text-blue-950">
            Targeted Enterprise:
            <select
              className="block w-full mt-1 border p-2 bg-white"
              value={selectedEnterprise}
              onChange={handleEnterpriseChange}
              disabled={enterprisesLoading}
            >
              <option value="">Select an enterprise</option>
              {enterprises.map((enterprise) => (
                <option key={enterprise.enterprise_id} value={enterprise.enterprise_id}>
                  {enterprise.enterprise_name}
                </option>
              ))}
            </select>
            {enterprisesLoading && <p>Loading enterprises...</p>}
            {enterprisesError && <p className="text-red-500">Error: {enterprisesError}</p>}
          </label>

          <label className="block flex-1 text-blue-950">
            Targeted Revenue:
            <select
              className="block w-full mt-1 border p-2 bg-white"
              value={revenueId}
              onChange={(e) => {
                const selectedDescription = descriptions.find(d => d.revenue_id.toString() === e.target.value);
                if (selectedDescription) {
                  handleTargetedRevenueChange(selectedDescription.description, e.target.value);
                }
              }}
              disabled={descriptionsLoading || !selectedEnterprise}
            >
              <option value="">Select targeted revenue</option>
              {descriptions.map((item) => (
                <option key={item.revenue_id} value={item.revenue_id}>
                  {item.description}
                </option>
              ))}
            </select>
            {descriptionsLoading && <p>Loading descriptions...</p>}
            {descriptionsError && <p className="text-red-500">Error: {descriptionsError}</p>}
          </label>

          <label className="block flex-1 text-blue-950">
            Statement Type:
            <select
              className="block w-full mt-1 border p-2 bg-white"
              value={statementType}
              onChange={(e) => onStatementTypeChange(e.target.value)}
              disabled={!isSelectionComplete}
            >
              <option value="revenue">Revenue</option>
              <option value="profit">Profit</option>
            </select>
          </label>

          <label className="block flex-1 text-blue-950">
            Choose the Year:
            <select
              className="block w-full mt-1 border p-2 bg-white"
              value={selectedYear}
              onChange={(e) => onYearChange(e.target.value)}
              disabled={!isSelectionComplete}
            >
              <option value={nextYear.toString()}>{nextYear}</option>
            </select>
          </label>

          <label className="block flex-1 text-blue-950">
            Started Month:
            <input
              type="text"
              className="block w-full mt-1 border p-2 bg-white"
              value={startedMonth}
              readOnly
              disabled={!isSelectionComplete}
            />
          </label>
        </div>
      </form>
      {!isSelectionComplete && (
        <p className="mt-4 text-yellow-600">
          Please select both an enterprise and a targeted revenue to enable all options.
        </p>
      )}
      {isSelectionComplete && (
        <p className="mt-4 text-green-600">
          Enterprise and targeted revenue selected. All options are now enabled.
        </p>
      )}
    </div>
  );
}

export default Options;