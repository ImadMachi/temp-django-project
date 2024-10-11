import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const fetchEnterprises = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/enterprise-industry/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching enterprises:", error);
    throw error;
  }
};

export const fetchValidationData = async (enterpriseId) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/agents/validation/${enterpriseId}/`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching validation data:", error);
    throw error;
  }
};

export const fetchHistoricalData = async (enterpriseId, description = null) => {
  try {
    let url = `${BASE_URL}/agents/historical-data/${enterpriseId}/`;
    if (description) {
      url += `?description=${encodeURIComponent(description)}`;
    }
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Error fetching historical data:", error);
    throw error;
  }
};

export const fetchAggregatedData = async (enterpriseId, description) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/agents/acp-t-produit/${enterpriseId}/`,
      {
        params: { description: description },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching aggregated data:", error);
    throw error;
  }
};

export const fetchEnterpriseData = async (
  enterpriseId,
  growthRate,
  description
) => {
  try {
    let url = `${BASE_URL}/agents/agent-pred-globale/${enterpriseId}/`;

    const params = new URLSearchParams({
      growth_rate: growthRate,
    });

    if (description) {
      params.append("description", description);
    }

    console.log("Fetching from URL:", `${url}?${params.toString()}`);

    const response = await axios.get(url, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching enterprise data:", error);
    if (error.response) {
      console.error("Error data:", error.response.data);
      console.error("Error status:", error.response.status);
      console.error("Error headers:", error.response.headers);
    } else if (error.request) {
      console.error("Error request:", error.request);
    } else {
      console.error("Error message:", error.message);
    }
    throw error;
  }
};

export const fetchUnitBasedRevenuePrediction = async (
  enterpriseId,
  growthRate,
  description
) => {
  try {
    let url = `${BASE_URL}/agents/unit-pred-revenu/${enterpriseId}/`;
    const params = new URLSearchParams({
      growth_rate: growthRate,
      description: description,
    });
    console.log("Fetching from URL:", `${url}?${params.toString()}`);
    const response = await axios.get(url, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching unit-based revenue prediction:", error);
    if (error.response) {
      console.error("Error data:", error.response.data);
      console.error("Error status:", error.response.status);
      console.error("Error headers:", error.response.headers);
    } else if (error.request) {
      console.error("Error request:", error.request);
    } else {
      console.error("Error message:", error.message);
    }
    throw error;
  }
};
export const fetchRevenueDescriptions = async (enterpriseId) => {
  try {
    const response = await fetch(
      `${BASE_URL}/revenue-descriptions/?enterprise_id=${enterpriseId}`
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching revenue descriptions:", error);
    throw error;
  }
};

export const fetchLatestOrderBook = async (enterpriseId) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/latest-orderbooks/${enterpriseId}/`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching latest order book:", error);
    throw error;
  }
};

export const fetchLatestOpportunityBook = async (enterpriseId) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/latest-opportunitybooks/${enterpriseId}/`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching latest opportunity book:", error);
    throw error;
  }
};
export const saveBulkIncomeDetail = async (data) => {
  try {
    const response = await axios.post(`${BASE_URL}/bulk-income-detail/`, data);
    return response.data;
  } catch (error) {
    console.error("Error saving bulk income detail:", error);
    throw error;
  }
};
