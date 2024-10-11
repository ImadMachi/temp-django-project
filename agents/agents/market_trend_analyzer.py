import logging
from typing import List, Dict, Tuple, Any, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
import re
from django.core.cache import cache

load_dotenv()


def clean_text(text: str) -> str:
    text = re.sub(r"[#*]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    matches = re.findall(r"(\w+\s+\w+(?:\s+\w+)?\s+[\d.]+%?)", text)
    return matches[0] if matches else text


class MarketTrendAnalyzer:
    def __init__(
        self,
        google_api_key: Optional[str] = None,
        num_trends: int = 5,
        num_stats: int = 5,
        cache_timeout: int = 3600,
    ):
        self.logger = logging.getLogger(__name__)
        if google_api_key is None:
            google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash", google_api_key=google_api_key
        )
        self.num_trends = num_trends
        self.num_stats = num_stats
        self.cache_timeout = cache_timeout

    def analyze_market_trends(
        self, industry_type: str, current_year: int, next_year: int
    ) -> Dict[str, Any]:
        try:
            content = self._fetch_industry_data(industry_type, current_year, next_year)
            trends, statistics = self._extract_trends_and_stats(
                content, industry_type, current_year, next_year
            )
            hypothesis, explanation = self._generate_hypothesis_and_explanation(
                industry_type, current_year, next_year, content
            )

            clean_trends = [clean_text(trend) for trend in trends if trend]
            clean_statistics = [clean_text(stat) for stat in statistics if stat]
            clean_hypothesis = clean_text(hypothesis)
            clean_explanation = clean_text(explanation)

            return {
                "trends": clean_trends[: self.num_trends],
                "statistics": clean_statistics[: self.num_stats],
                "hypothesis": self._extract_numeric_hypothesis(clean_hypothesis),
                "explanation": clean_explanation,
            }
        except Exception as e:
            self.logger.error(
                f"Unexpected error in analyze_market_trends: {str(e)}", exc_info=True
            )
            return self._generate_fallback_analysis(
                industry_type, current_year, next_year
            )

    def _fetch_industry_data(
        self, industry_type: str, current_year: int, next_year: int
    ) -> str:
        # Sanitize industry_type for use in cache key
        sanitized_industry_type = re.sub(r"[^\w]+", "_", industry_type)
        cache_key = (
            f"industry_data_{sanitized_industry_type}_{current_year}_{next_year}"
        )
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        try:
            query = f"{industry_type} industry trends statistics financial analysis {current_year} {next_year} forecast"
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            snippets = [result.get_text() for result in soup.select(".g")]
            fetched_data = " ".join(snippets[:10])
            cache.set(cache_key, fetched_data, self.cache_timeout)
            return fetched_data
        except requests.RequestException as e:
            self.logger.warning(f"Failed to fetch market trends: {str(e)}")
            return f"Unable to fetch real-time data. Analyzing general trends for {industry_type} industry for {current_year}-{next_year}."

    def _extract_trends_and_stats(
        self, content: str, industry_type: str, current_year: int, next_year: int
    ) -> Tuple[List[str], List[str]]:
        prompt = PromptTemplate(
            input_variables=[
                "content",
                "industry_type",
                "current_year",
                "next_year",
                "num_trends",
                "num_stats",
            ],
            template="""
            As a financial analyst specializing in the {industry_type} industry, analyze the following information for {current_year} and {next_year}:

            {content}

            Provide two lists:
            1. A list of {num_trends} key market trends specific to the {industry_type} industry, focusing on the transition from {current_year} to {next_year}.
            2. A list of {num_stats} statistical points or numerical facts about the {industry_type} industry, with emphasis on {next_year} forecasts.

            For the trends, focus on:
            - Technological disruptions expected in {next_year}
            - Anticipated shifts in market demand or consumer behavior
            - Emerging business models or strategies for {next_year}
            - Regulatory changes impacting financials in the coming year
            - Economic factors affecting profitability in the transition to {next_year}
            - Expected changes in competitive landscape
            - Key financial metrics or ratios gaining importance in {next_year}

            For the statistical points, prioritize:
            - Projected market size and CAGR for {next_year}
            - Forecasted industry average P/E ratio for {next_year}
            - Expected median profit margins in {next_year}
            - Anticipated revenue distribution among key players
            - Projected capital expenditure trends for {next_year}
            - Forecasted R&D spending as a percentage of revenue
            - Industry-specific financial benchmarks expected for {next_year}

            Ensure each point is tailored to the {industry_type} industry and reflects the transition from {current_year} to {next_year}. Use precise figures where available, or provide reasonable estimates based on industry forecasts.

            Format your response as two separate lists, each with bullet points.
            First list: Trends
            Second list: Statistics
            """,
        )
        try:
            chain = prompt | self.llm
            response = chain.invoke(
                {
                    "content": content,
                    "industry_type": industry_type,
                    "current_year": current_year,
                    "next_year": next_year,
                    "num_trends": self.num_trends,
                    "num_stats": self.num_stats,
                }
            )
            all_points = [
                point.strip() for point in response.strip().split("\n") if point.strip()
            ]
            return all_points[: self.num_trends], all_points[self.num_trends :]
        except Exception as e:
            self.logger.error(
                f"Error in _extract_trends_and_stats: {str(e)}", exc_info=True
            )
            return [], []

    def _generate_hypothesis_and_explanation(
        self, industry_type: str, current_year: int, next_year: int, content: str
    ) -> Tuple[str, str]:
        prompt = PromptTemplate(
            input_variables=["industry_type", "current_year", "next_year", "content"],
            template="""
            As a financial analyst specializing in the {industry_type} industry, based on the following information:

            {content}

            1. Generate a brief revenue growth hypothesis with a specific percentage for the {industry_type} industry in {next_year}, considering the transition from {current_year}.
            2. Provide a short explanation for this hypothesis, considering key financial drivers and market conditions expected in the transition from {current_year} to {next_year}.

            Format your response as:
            Hypothesis: [Your hypothesis here]
            Explanation: [Your explanation here]
            """,
        )
        try:
            chain = prompt | self.llm
            response = chain.invoke(
                {
                    "industry_type": industry_type,
                    "current_year": current_year,
                    "next_year": next_year,
                    "content": content,
                }
            )
            hypothesis, explanation = response.split("Explanation:")
            return hypothesis.replace("Hypothesis:", "").strip(), explanation.strip()
        except Exception as e:
            self.logger.error(
                f"Error in _generate_hypothesis_and_explanation: {str(e)}",
                exc_info=True,
            )
            return (
                f"0% growth for {industry_type} in {next_year}",
                f"Insufficient data to project growth from {current_year} to {next_year}.",
            )

    def _extract_numeric_hypothesis(self, hypothesis: str) -> float:
        try:
            return float(re.findall(r"[-+]?\d*\.?\d+", hypothesis)[0])
        except (IndexError, ValueError):
            self.logger.warning(
                f"Failed to extract numeric hypothesis from: {hypothesis}"
            )
            return 0.0

    def _generate_fallback_analysis(
        self, industry_type: str, current_year: int, next_year: int
    ) -> Dict[str, Any]:
        return {
            "trends": [
                f"Increasing digitalization in {industry_type}",
                f"Growing focus on efficiency and cost-cutting measures in {industry_type}",
                f"Rising importance of data-driven decision making in {industry_type}",
                f"Shift towards sustainable practices in {industry_type}",
                f"Emerging challenges in cybersecurity and data protection for {industry_type}",
            ],
            "statistics": [
                f"The global {industry_type} market is projected to reach $X billion in {next_year}",
                f"CAGR for {industry_type} is expected to be Y% from {current_year} to {next_year}",
                f"Top players in {industry_type} are forecasted to hold Z% market share in {next_year}",
                f"R&D spending in {industry_type} is projected to increase by W% in {next_year}",
                f"Average profit margins in {industry_type} are expected to be V% in {next_year}",
            ],
            "hypothesis": 0.0,
            "explanation": f"Unable to generate specific analysis for {industry_type} for {next_year}. Using generic industry trends and statistics based on {current_year} data.",
        }
