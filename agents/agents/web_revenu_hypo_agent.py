import random
from datetime import datetime
from typing import Dict
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()


class WebRevenuHypoAgent:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-pro", google_api_key=self.google_api_key
        )

    def execute(
        self,
        industry_type: str,
        growth_rate: float,
        enterprise_info: Dict,
        prediction_year: int,
    ) -> Dict:
        try:
            industry_data = self.fetch_industry_data(industry_type, prediction_year)
            monthly_predictions = self.generate_monthly_predictions(
                industry_type,
                growth_rate,
                enterprise_info,
                industry_data,
                prediction_year,
            )
            analysis = self.generate_analysis(
                industry_type,
                growth_rate,
                enterprise_info,
                monthly_predictions,
                industry_data,
                prediction_year,
            )

            return {
                "prediction_year": prediction_year,
                "monthly_predictions": monthly_predictions,
                "enterprise_info": enterprise_info,
            }
        except Exception as e:
            return {"error": f"Failed to generate predictions: {str(e)}"}

    def fetch_industry_data(self, industry_type: str, prediction_year: int) -> Dict:
        query = f"{industry_type} industry trends statistics financial analysis forecast {prediction_year}"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = [result.get_text() for result in soup.select(".g")]
        content = " ".join(snippets[:10])

        prompt = PromptTemplate(
            input_variables=["industry_type", "prediction_year", "content"],
            template="""
            As a financial analyst, extract key information about the {industry_type} industry for the year {prediction_year} from the following content:

            {content}

            Provide the following information:
            1. Estimated average annual revenue for a company in this industry in {prediction_year}
            2. Projected industry growth rate for {prediction_year}
            3. Key trends affecting the industry in {prediction_year} (comma-separated list)
            4. Potential challenges or risks for {prediction_year} (comma-separated list)
            5. Seasonality factors for {prediction_year} (comma-separated list of 12 numbers, one for each month, or 'N/A' if not applicable)

            Format your response as a JSON object with keys: average_revenue, growth_rate, trends, challenges, seasonality.
            Use "N/A" if you can't find specific information for any field.
            """,
        )

        response = self.llm(
            prompt.format(
                industry_type=industry_type,
                prediction_year=prediction_year,
                content=content,
            )
        )

        try:
            parsed_data = json.loads(response)
        except json.JSONDecodeError:
            parsed_data = {}
            patterns = {
                "average_revenue": r'"average_revenue":\s*"([^"]+)"',
                "growth_rate": r'"growth_rate":\s*"([^"]+)"',
                "trends": r'"trends":\s*"([^"]+)"',
                "challenges": r'"challenges":\s*"([^"]+)"',
                "seasonality": r'"seasonality":\s*"([^"]+)"',
            }
            for key, pattern in patterns.items():
                match = re.search(pattern, response)
                parsed_data[key] = match.group(1) if match else "N/A"

        default_data = {
            "average_revenue": "N/A",
            "growth_rate": "N/A",
            "trends": f"Digitalization, AI adoption, cloud computing in {prediction_year}",
            "challenges": f"Economic uncertainty, cybersecurity threats, talent shortage in {prediction_year}",
            "seasonality": "N/A",
        }

        final_data = {**default_data, **parsed_data}

        return final_data

    def generate_monthly_predictions(
        self,
        industry_type: str,
        growth_rate: float,
        enterprise_info: Dict,
        industry_data: Dict,
        prediction_year: int,
    ) -> Dict[str, float]:
        base_revenue = (
            float(industry_data["average_revenue"].replace("$", "").replace(",", ""))
            if industry_data["average_revenue"] != "N/A"
            else 100000
        )
        industry_growth = (
            float(industry_data["growth_rate"].strip("%")) / 100
            if industry_data["growth_rate"] != "N/A"
            else 0.05
        )

        combined_growth_rate = (growth_rate + industry_growth) / 2

        seasonality = (
            [float(x) for x in industry_data["seasonality"].split(",")]
            if industry_data["seasonality"] != "N/A"
            else [1.0] * 12
        )

        employees_count = enterprise_info.get("employees_count", 1)
        base_revenue *= max(1, (employees_count / 10) ** 0.5)

        founding_date = datetime.fromisoformat(
            enterprise_info["founding_date"].replace("Z", "+00:00")
        )
        company_age = prediction_year - founding_date.year
        age_factor = min(1.5, max(0.5, (company_age + 1) ** 0.3))
        base_revenue *= age_factor

        monthly_predictions = {}
        for month in range(1, 13):
            monthly_growth = (1 + combined_growth_rate) ** (month / 12)
            seasonal_factor = seasonality[month - 1] if len(seasonality) == 12 else 1.0
            random_factor = random.uniform(0.95, 1.05)
            revenue = base_revenue * monthly_growth * seasonal_factor * random_factor
            monthly_predictions[f"{prediction_year}-{month:02d}"] = round(revenue, 2)

        return monthly_predictions

    def generate_analysis(
        self,
        industry_type: str,
        growth_rate: float,
        enterprise_info: Dict,
        predictions: Dict[str, float],
        industry_data: Dict,
        prediction_year: int,
    ) -> str:
        prompt = PromptTemplate(
            input_variables=[
                "industry_type",
                "growth_rate",
                "enterprise_info",
                "predictions",
                "industry_data",
                "prediction_year",
            ],
            template="""
        As a financial analyst, provide an analysis of the revenue predictions for {enterprise_info[enterprise_name]} in the {industry_type} industry for the year {prediction_year}.
        Use the following information:

        Company Information:
        {enterprise_info}

        Revenue Predictions for {prediction_year}:
        {predictions}

        Industry Data for {prediction_year}:
        {industry_data}

        Company's Expected Growth Rate: {growth_rate:.1%}

        Provide a detailed analysis covering:
        1. Overall revenue projection for {prediction_year} and how it compares to the industry average (if available)
        2. Monthly revenue trends in {prediction_year} and their alignment with industry seasonality (if available)
        3. Potential impact of industry trends and challenges on the company in {prediction_year}
        4. How the company's age and size might influence its performance in {prediction_year}
        5. Recommendations for capitalizing on opportunities or mitigating risks in {prediction_year}
        6. Confidence level in the predictions and factors that could significantly alter the forecast

        Your analysis should be detailed, insightful, and about 300-350 words long.
        """,
        )

        analysis = self.llm(
            prompt.format(
                industry_type=industry_type,
                growth_rate=growth_rate,
                enterprise_info=enterprise_info,
                predictions=predictions,
                industry_data=industry_data,
                prediction_year=prediction_year,
            )
        )

        return analysis
