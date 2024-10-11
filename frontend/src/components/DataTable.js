// DataTable.js
import React, { useMemo } from 'react';
import { useTable } from 'react-table';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const DataTable = ({ selectedPrediction, localEnterpriseData, unitBasedData, editedData, handleCellEdit, getData }) => {
  const tableData = useMemo(() => {
    if (selectedPrediction === 'unit_sold' && unitBasedData) {
      const years = [...new Set(unitBasedData.historical_data.map(item => item.year))].sort().slice(-2);
      const [yearBeforeLast, lastYear] = years;

      return MONTHS.map((month, index) => {
        const monthIndex = index + 1;
        const yearBeforeLastData = unitBasedData.historical_data.find(item => item.year === yearBeforeLast && item.month === monthIndex);
        const lastYearData = unitBasedData.historical_data.find(item => item.year === lastYear && item.month === monthIndex);
        const predictedData = unitBasedData.next_year_prediction[index];

        return {
          month,
          'Year Before Last': yearBeforeLastData?.real_income ?? 'N/A',
          'Last Year': lastYearData?.real_income ?? 'N/A',
          [`${unitBasedData.next_year} (Predicted)`]: predictedData?.predicted_income ?? 'N/A',
        };
      });
    } else {
      const { yearBeforeLast, lastYear, predicted } = getData();
      return MONTHS.map((month, index) => ({
        month,
        'Year Before Last': yearBeforeLast[index],
        'Last Year': lastYear[index],
        [`${localEnterpriseData?.prediction_year || 'Future'} (Predicted)`]: editedData[index] ?? predicted[index],
      }));
    }
  }, [localEnterpriseData, selectedPrediction, editedData, unitBasedData, getData]);

  const columns = useMemo(() => [
    { Header: 'Month', accessor: 'month' },
    { Header: 'Year Before Last', accessor: 'Year Before Last' },
    { Header: 'Last Year', accessor: 'Last Year' },
    {
      Header: `${selectedPrediction === 'unit_sold' && unitBasedData ? unitBasedData.next_year : localEnterpriseData?.prediction_year || 'Future'} (Predicted)`,
      accessor: `${selectedPrediction === 'unit_sold' && unitBasedData ? unitBasedData.next_year : localEnterpriseData?.prediction_year || 'Future'} (Predicted)`,
      Cell: ({ row, value }) => (
        <input
          type="number"
          value={value}
          onChange={(e) => handleCellEdit(row.index, e.target.value)}
          className="w-full p-1 border border-gray-300 rounded bg-white !text-gray-800"
        />
      )
    },
  ], [localEnterpriseData, selectedPrediction, unitBasedData, handleCellEdit]);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data: tableData });

  return (
    <table {...getTableProps()} className="table table-xs table-pin-rows table-pin-cols w-full !text-gray-800">
      <thead className="bg-white border-b">
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()} className="bg-white">
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()} className="border p-2 text-left font-semibold !text-gray-800 bg-white">
                {column.render('Header')}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()} className="!text-gray-800">
        {rows.map(row => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => (
                <td {...cell.getCellProps()} className="border p-2 !text-gray-800">
                  {cell.render('Cell')}
                </td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default DataTable;