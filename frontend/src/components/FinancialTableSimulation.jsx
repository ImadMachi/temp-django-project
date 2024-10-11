import { PercentageOutlined } from "@ant-design/icons";
import { Button, Card, Col, Input, Row, Space, Table, Typography, message } from "antd";
import React, { useEffect, useState } from "react";
import { useLocation } from 'react-router-dom';
import AdditionalInfoCard from './AdditionalInfoCard';
import useOrderBook from "../hooks/useOrderBook";
import useOpportunityBook from "../hooks/useOpportunityBook";
import useFinancialSimulation from "../hooks/useFinancialSimulation";

const { Title } = Typography;

function FinancialTableSimulation() {
  const location = useLocation();
  const enterpriseId = location.state?.enterpriseId;

  const [simulationInput, setSimulationInput] = useState(false);
  const [data, setData] = useState({
    categories: {},
    revenueIds: {},
    totalRevenus: Array(12).fill(0),
    totalRevenusSimuler: Array(12).fill(0),
    Totaltotaux: 0,
    totalPourcentages: {},
    percentages: {},
    totalSimuler: {},
    totalsSimuler: 0,
    categoriesSimuler: {},
  });

  const { orderBook, loading: orderLoading, error: orderError } = useOrderBook(enterpriseId);
  const { opportunityBook, loading: oppLoading, error: oppError } = useOpportunityBook(enterpriseId);
  const { saveSimulation, loading: saveLoading, error: saveError } = useFinancialSimulation();

  const [additionalInfo, setAdditionalInfo] = useState({
    carnetDeCommande: 0,
    pourcentageClosing: 0,
    carnetOppTotal: 0
  });

  useEffect(() => {
    if (orderBook && opportunityBook) {
      setAdditionalInfo({
        carnetDeCommande: orderBook.latest_total || 0,
        pourcentageClosing: opportunityBook.pourcentage_closing || 0.2,
        carnetOppTotal: opportunityBook.latest_total || 0
      });
    }
  }, [orderBook, opportunityBook]);

  useEffect(() => {
    const storedData = JSON.parse(localStorage.getItem("approvedPredictions")) || [];

    if (storedData.length > 0) {
      const categories = {};
      const revenueIds = {};
      storedData.forEach((enterprise) => {
        const { targetedRevenue, revenueId, tableData } = enterprise;
        categories[targetedRevenue] = tableData.map((month) => month.edited);
        revenueIds[targetedRevenue] = revenueId;
      });

      setData((prevData) => ({
        ...prevData,
        categories,
        revenueIds,
        categoriesSimuler: categories,
      }));
    }
  }, []);

  const updateCell = (category, monthIndex, value) => {
    setData((prevData) => {
      const newData = { ...prevData };
      newData.categories[category][monthIndex] = parseFloat(value) || 0;
      return newData;
    });
    setTimeout(calculateTotals, 0);
  };

  const calculateTotalPercentage = (category) => {
    const categoryData = data.categories[category];
    const total = categoryData.reduce((acc, curr) => acc + curr, 0);
    return Math.round(total > 0 ? 100 : 0);
  };

  const calculateTotals = React.useCallback(() => {
    setData((prevData) => {
      const categories = Object.keys(prevData.categories);
      const newTotalRevenus = Array(12).fill(0);
      const newTotalRevenusSimuler = Array(12).fill(0);
      let Totaltotaux = 0;
      const totalPourcentages = {};
      const totalSimuler = {};
      const newcategoriesSimuler = {};
      const newPercentages = {};

      categories.forEach((category) => {
        const categoryTotal = prevData.categories[category].reduce(
          (acc, curr) => acc + curr,
          0
        );
        Totaltotaux += categoryTotal;

        newPercentages[category] = prevData.categories[category].map((value) =>
          categoryTotal ? (value / categoryTotal) * 100 : 0
        );
      });

      categories.forEach((category) => {
        const categoryTotal = prevData.categories[category].reduce(
          (acc, curr) => acc + curr,
          0
        );
        totalPourcentages[category] = (categoryTotal / Totaltotaux) * 100;
        totalSimuler[category] = Math.round(
          (prevData.totalsSimuler * totalPourcentages[category]) / 100
        );

        newcategoriesSimuler[category] = newPercentages[category].map((value) =>
          Math.round((totalSimuler[category] * value) / 100)
        );
      });

      newTotalRevenus.forEach((_, index) => {
        let total = 0;
        categories.forEach((category) => {
          total += prevData.categories[category][index];
        });
        newTotalRevenus[index] = total;
      });

      newTotalRevenusSimuler.forEach((_, index) => {
        let total = 0;
        categories.forEach((category) => {
          total += newcategoriesSimuler[category][index];
        });
        newTotalRevenusSimuler[index] = total;
      });

      return {
        ...prevData,
        totalRevenus: newTotalRevenus,
        totalRevenusSimuler: newTotalRevenusSimuler,
        Totaltotaux,
        totalPourcentages,
        totalSimuler,
        percentages: newPercentages,
        categoriesSimuler: newcategoriesSimuler,
      };
    });
  }, []);

  const handleSimulatedData = (value) => {
    setData((prevData) => ({
      ...prevData,
      totalsSimuler: parseFloat(value) || 0,
    }));
  };

  const handleSimulate = () => {
    setSimulationInput(true);
  };

  const handleCancel = () => {
    setSimulationInput(false);
  };

  const handleApprove = async () => {
    const simulationData = {
      income_details: Object.entries(simulationInput ? data.categoriesSimuler : data.categories).map(([category, values]) => ({
        enterpriseId: enterpriseId,
        revenueId: data.revenueIds[category],
        category: category,
        predictionYear: new Date().getFullYear() + 1,
        ...values.reduce((acc, value, index) => ({ ...acc, [`month${index + 1}`]: value }), {}),
        total: values.reduce((acc, curr) => acc + curr, 0)
      }))
    };

    try {
      await saveSimulation(simulationData);
      message.success('Simulation approved and saved successfully');
    } catch (error) {
      message.error('Failed to save simulation');
    }
  };

  useEffect(() => {
    calculateTotals();
  }, [data.categories, data.totalsSimuler, calculateTotals]);

  const columns = [
    {
      title: "Type Revenus",
      dataIndex: "category",
      key: "category",
      fixed: "left",
      width: 120,
    },
    ...[
      "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ].map((month, i) => ({
      title: month,
      dataIndex: `month${i}`,
      key: `month${i}`,
      width: 100,
      render: (text, record) => {
        if (record.isPercentage) {
          return <span>{Math.round(text)}%</span>;
        }
        if (record.key.includes("total-")) {
          return <span>{Math.round(text)}</span>;
        }
        return (
          <Input
            type="number"
            value={text}
            onChange={(e) => updateCell(record.category, i, e.target.value)}
            style={{ width: "100%" }}
          />
        );
      },
    })),
    {
      title: "Total",
      dataIndex: "total",
      key: "total",
      width: 100,
      render: (text, record) => (
        <span style={{ fontWeight: "bold" }}>
          {record.isPercentage ? `${text}%` : text}
        </span>
      ),
    },
    {
      title: "Total Simuler",
      dataIndex: "totalSimuler",
      key: "totalSimuler",
      width: 120,
    },
    {
      title: "Pourcentage",
      dataIndex: "percentage",
      key: "percentage",
      width: 120,
      render: (text) => <span>{text}</span>,
    },
  ];

  const dataSource = Object.entries(
    simulationInput ? data.categoriesSimuler : data.categories
  ).flatMap(([category, values]) => [
    {
      key: `${category}-percentage`,
      category: <PercentageOutlined />,
      isPercentage: true,
      ...values.reduce(
        (acc, _, i) => ({
          ...acc,
          [`month${i}`]: data.percentages[category]?.[i] || 0,
        }),
        {}
      ),
      total: calculateTotalPercentage(category),
      totalSimuler: "",
      percentage: "",
      revenueId: data.revenueIds[category],
    },
    {
      key: category,
      category,
      isPercentage: false,
      ...values.reduce(
        (acc, value, i) => ({ ...acc, [`month${i}`]: value }),
        {}
      ),
      total: values.reduce((acc, curr) => acc + curr, 0),
      totalSimuler: data.totalSimuler[category],
      percentage: `${data.totalPourcentages[category]?.toFixed(2)}%`,
      revenueId: data.revenueIds[category],
    },
  ]);

  dataSource.push({
    key: "total-revenus",
    category: "Total revenus",
    isPercentage: false,
    ...data.totalRevenus.reduce(
      (acc, value, i) => ({ ...acc, [`month${i}`]: value }),
      {}
    ),
    total: data.Totaltotaux,
    totalSimuler: (
      <Input
        type="number"
        value={data.totalsSimuler}
        onChange={(e) => handleSimulatedData(e.target.value)}
        style={{ width: "100%" }}
      />
    ),
    percentage: "100%",
  });

  dataSource.push({
    key: "total-simuler",
    category: "Total simuler",
    isPercentage: false,
    ...data.totalRevenusSimuler.reduce(
      (acc, value, i) => ({ ...acc, [`month${i}`]: value }),
      {}
    ),
    total: "",
    totalSimuler: "",
    percentage: "",
  });

  if (orderLoading || oppLoading) {
    return <div>Loading...</div>;
  }

  if (orderError || oppError) {
    return <div>Error: {orderError || oppError}</div>;
  }

  return (
    <Card style={{ margin: "20px" }}>
      <Title level={2}>Financial Table Simulation</Title>
  
      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        scroll={{ x: "max-content" }}
        bordered
        size="small"
      />
  
      <div style={{ display: 'flex', marginTop: "20px" }}>
        <Card 
          title="Simulation Controls" 
          style={{ flex: '0 0 60%', marginRight: '20px' }}
        >
          <Row gutter={[16, 16]} align="middle">
            <Col xs={24} sm={12} md={8} lg={6}>
              <Input
                type="number"
                value={data.totalsSimuler}
                onChange={(e) => handleSimulatedData(e.target.value)}
                placeholder="Enter total simuler"
                size="large"
              />
            </Col>
            <Col xs={24} sm={12} md={16} lg={18}>
              <Space>
                <Button size="large" type="primary" onClick={handleSimulate}>
                  Simuler
                </Button>
                <Button
                  size="large"
                  disabled={!simulationInput}
                  onClick={handleCancel}
                >
                  Annuler
                </Button>
                <Button 
                  size="large" 
                  type="primary" 
                  onClick={handleApprove}
                  loading={saveLoading}
                >
                  Approuver
                </Button>
              </Space>
            </Col>
          </Row>
        </Card>
  
        <AdditionalInfoCard data={additionalInfo} style={{ flex: '0 0 38%' }} />
      </div>
      {saveError && <div style={{ color: 'red', marginTop: '10px' }}>Error: {saveError}</div>}
    </Card>
  );
}

export default FinancialTableSimulation;