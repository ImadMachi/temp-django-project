import React from 'react';
import { Card, Table } from 'antd';

const AdditionalInfoCard = ({ data }) => {
  const carnetOpportunite = data.carnetOppTotal * data.pourcentageClosing;
  const total = parseFloat(data.carnetDeCommande) + parseFloat(carnetOpportunite);


  const dataSource = [
    { key: 'carnetCommande', label: 'Carnet de commande', value: data.carnetDeCommande.toLocaleString() },
    { key: 'pourcentage', label: 'Pourcentage du closing des opportunités', value: `${(data.pourcentageClosing * 100).toFixed(1)}%` },
    { key: 'carnetOppTotal', label: 'Carnet Opp Total', value: data.carnetOppTotal.toLocaleString() },
    { key: 'carnetOpportunite', label: "Carnet d'Opportunité", value: carnetOpportunite.toLocaleString() },
    { key: 'total', label: '', value: total.toLocaleString(), isTotal: true },
  ];

  const columns = [
    { 
      title: 'Label', 
      dataIndex: 'label', 
      key: 'label',
      render: (text, record) => record.isTotal ? '' : text
    },
    { 
      title: 'Value', 
      dataIndex: 'value', 
      key: 'value', 
      align: 'right',
      render: (text, record) => (
        <span style={record.isTotal ? { fontWeight: 'bold', backgroundColor: '#4CAF50', color: 'white', padding: '2px 5px' } : {}}>
          {text}
        </span>
      )
    },
  ];

  return (
    <Card title="Additional Information" style={{ marginTop: '20px', width: '300px', float: 'right' }}>
      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        showHeader={false}
        size="small"
      />
    </Card>
  );
};

export default AdditionalInfoCard;