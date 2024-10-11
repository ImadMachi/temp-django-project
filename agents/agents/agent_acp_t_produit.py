import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from django.db.models import Sum, Avg, StdDev
from financial_data.models import RevenuesView, EnterpriseIndustryView
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from collections import defaultdict
from datetime import datetime
import traceback
from decimal import Decimal


def safe_float(value):
    try:
        float_value = float(value)
        return float_value if np.isfinite(float_value) else None
    except (ValueError, TypeError):
        return None


class AgentACP_T_produit:
    @staticmethod
    def execute(enterprise_id, description):
        try:
            target_enterprise = EnterpriseIndustryView.objects.get(
                enterprise_id=enterprise_id
            )

            if not target_enterprise.industry_type_label:
                return {"error": "Unable to determine industry type for the enterprise"}

            related_enterprises = EnterpriseIndustryView.objects.filter(
                industry_type_label=target_enterprise.industry_type_label,
                enterprise_active=True,
            )

            aggregated_data = AgentACP_T_produit._get_aggregated_data(
                related_enterprises, description
            )

            if isinstance(aggregated_data, dict) and "error" in aggregated_data:
                return {"error": aggregated_data["error"]}

            pca_result, pca_coefficients = AgentACP_T_produit._perform_pca(
                aggregated_data
            )
            seasonal_trends = AgentACP_T_produit._identify_seasonal_trends(
                aggregated_data
            )
            anomalies = AgentACP_T_produit._detect_anomalies(
                target_enterprise.enterprise_id, aggregated_data, description
            )
            risk_assessment = AgentACP_T_produit._assess_risk(
                target_enterprise.enterprise_id, aggregated_data, description
            )
            performance_evaluation = AgentACP_T_produit._evaluate_performance(
                target_enterprise.enterprise_id, aggregated_data, description
            )
            adjusted_budgets = AgentACP_T_produit._adjust_budgets(
                enterprise_id, aggregated_data, pca_coefficients, description
            )
            trend_analysis = AgentACP_T_produit._analyze_trends(
                aggregated_data)
            market_share = AgentACP_T_produit._estimate_market_share(
                target_enterprise.enterprise_id, aggregated_data, description
            )

        except Exception as e:
            error_traceback = traceback.format_exc()
            return {
                "error": f"Error during data analysis: {str(e)}",
                "traceback": error_traceback,
            }

        return {
            "industry_type": target_enterprise.industry_type_label,
            "aggregated_data": aggregated_data,
            "pca_coefficients": pca_result,
            "seasonal_trends": seasonal_trends,
            "anomalies": anomalies,
            "risk_assessment": risk_assessment,
            "performance_evaluation": performance_evaluation,
            "adjusted_budgets": adjusted_budgets,
            "trend_analysis": trend_analysis,
            "market_share": market_share,
        }

    @staticmethod
    def _get_aggregated_data(related_enterprises, description):
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        enterprise_count = defaultdict(int)
        current_year = datetime.now().year

        for enterprise in related_enterprises:
            try:
                revenues = RevenuesView.objects.filter(
                    enterprise_id=enterprise.enterprise_id, description=description
                )
                for revenue in revenues:
                    try:
                        year = int(revenue.year)
                        month = int(revenue.month)
                        if year <= current_year:
                            enterprise_count[year] += 1
                            data["real"][year][month].append(
                                safe_float(revenue.real_income)
                            )
                            data["budget"][year][month].append(
                                safe_float(revenue.expected_income)
                            )
                    except (ValueError, TypeError, AttributeError) as e:
                        print(
                            f"Error processing revenue data for enterprise {
                                enterprise.enterprise_id}: {e}"
                        )
                        continue
            except Exception as e:
                print(
                    f"Error retrieving revenue data for enterprise {
                        enterprise.enterprise_id}: {e}"
                )
                continue

        if not enterprise_count:
            return {"error": "No valid revenue data found for the related enterprises"}

        aggregated_data = {
            "years": sorted(
                [year for year in enterprise_count.keys() if year <= current_year]
            ),
            "aggregatedAverageReals": {},
            "aggregatedAverageBudgets": {},
        }

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

        for year in aggregated_data["years"]:
            aggregated_data["aggregatedAverageReals"][year] = []
            aggregated_data["aggregatedAverageBudgets"][year] = []
            for month in range(1, 13):
                real_values = [v for v in data["real"]
                               [year][month] if v is not None]
                budget_values = [
                    v for v in data["budget"][year][month] if v is not None
                ]
                aggregated_data["aggregatedAverageReals"][year].append(
                    {
                        "month": months[month - 1],
                        "value": safe_float(
                            sum(real_values) /
                            len(real_values) if real_values else 0
                        ),
                    }
                )
                aggregated_data["aggregatedAverageBudgets"][year].append(
                    {
                        "month": months[month - 1],
                        "value": safe_float(
                            sum(budget_values) / len(budget_values)
                            if budget_values
                            else 0
                        ),
                    }
                )

        return aggregated_data

    @staticmethod
    def _perform_pca(aggregated_data):
        data_matrix = []
        for year in aggregated_data["years"]:
            year_data = [
                safe_float(month["value"])
                for month in aggregated_data["aggregatedAverageReals"][year]
            ]
            year_data = [v for v in year_data if v is not None]
            if year_data:
                data_matrix.append(year_data)

        if not data_matrix or len(data_matrix) < 2:
            return [], []

        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(data_matrix)

        pca = PCA(n_components=1)
        pca_result = pca.fit_transform(normalized_data)

        coefficients = pca_result[:, 0]
        sum_abs_coefficients = np.sum(np.abs(coefficients))
        if sum_abs_coefficients != 0:
            coefficients = coefficients / sum_abs_coefficients
        else:
            coefficients = np.zeros_like(coefficients)

        return [[safe_float(v) for v in pca_result.flatten()]], [
            safe_float(v) for v in coefficients
        ]

    @staticmethod
    def _identify_seasonal_trends(aggregated_data):
        seasonal_trends = {}
        for year in aggregated_data["years"]:
            values = [
                safe_float(month["value"])
                for month in aggregated_data["aggregatedAverageReals"][year]
            ]
            values = [v for v in values if v is not None]
            if len(values) >= 24 and any(values):
                decomposition = seasonal_decompose(
                    values, model="additive", period=12)
                seasonal_trends[year] = [
                    safe_float(v) for v in decomposition.seasonal.tolist()
                ]
            else:
                seasonal_trends[year] = None
        return seasonal_trends

    @staticmethod
    def _detect_anomalies(enterprise_id, aggregated_data, description):
        enterprise_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, description=description
        )
        anomalies = {}
        for year in aggregated_data["years"]:
            enterprise_values = [
                safe_float(revenue.real_income)
                for revenue in enterprise_data.filter(year=str(year))
            ]
            enterprise_values = [v for v in enterprise_values if v is not None]
            industry_values = [
                safe_float(month["value"])
                for month in aggregated_data["aggregatedAverageReals"][year]
            ]
            industry_values = [v for v in industry_values if v is not None]
            if (
                len(enterprise_values) == 12
                and len(industry_values) == 12
                and any(enterprise_values)
            ):
                z_scores = stats.zscore(enterprise_values)
                anomalies[year] = [
                    i for i, z in enumerate(z_scores) if abs(z) > 2]
            else:
                anomalies[year] = None
        return anomalies

    @staticmethod
    def _assess_risk(enterprise_id, aggregated_data, description):
        enterprise_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, description=description
        )
        risk_assessment = {}
        for year in aggregated_data["years"]:
            enterprise_values = [
                safe_float(revenue.real_income)
                for revenue in enterprise_data.filter(year=str(year))
            ]
            enterprise_values = [v for v in enterprise_values if v is not None]
            industry_values = [
                safe_float(month["value"])
                for month in aggregated_data["aggregatedAverageReals"][year]
            ]
            industry_values = [v for v in industry_values if v is not None]
            if (
                len(enterprise_values) == 12
                and len(industry_values) == 12
                and any(enterprise_values)
                and any(industry_values)
            ):
                enterprise_volatility = safe_float(
                    np.std(enterprise_values) / np.mean(enterprise_values)
                    if np.mean(enterprise_values) != 0
                    else None
                )
                industry_volatility = safe_float(
                    np.std(industry_values) / np.mean(industry_values)
                    if np.mean(industry_values) != 0
                    else None
                )
                relative_risk = safe_float(
                    enterprise_volatility / industry_volatility
                    if industry_volatility and industry_volatility != 0
                    else None
                )
                risk_assessment[year] = {
                    "enterprise_volatility": enterprise_volatility,
                    "industry_volatility": industry_volatility,
                    "relative_risk": relative_risk,
                }
            else:
                risk_assessment[year] = None
        return risk_assessment

    @staticmethod
    def _evaluate_performance(enterprise_id, aggregated_data, description):
        enterprise_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, description=description
        )
        performance_evaluation = {}
        for year in aggregated_data["years"]:
            enterprise_real = sum(
                safe_float(revenue.real_income) or 0
                for revenue in enterprise_data.filter(year=str(year))
            )
            enterprise_budget = sum(
                safe_float(revenue.expected_income) or 0
                for revenue in enterprise_data.filter(year=str(year))
            )
            industry_real = sum(
                safe_float(month["value"]) or 0
                for month in aggregated_data["aggregatedAverageReals"][year]
            )
            industry_budget = sum(
                safe_float(month["value"]) or 0
                for month in aggregated_data["aggregatedAverageBudgets"][year]
            )

            if enterprise_budget != 0 and industry_budget != 0 and industry_real != 0:
                performance_evaluation[year] = {
                    "enterprise_budget_accuracy": safe_float(
                        enterprise_real / enterprise_budget
                    ),
                    "industry_budget_accuracy": safe_float(
                        industry_real / industry_budget
                    ),
                    "relative_performance": safe_float(enterprise_real / industry_real),
                }
            else:
                performance_evaluation[year] = None
        return performance_evaluation

    @staticmethod
    def _analyze_trends(aggregated_data):
        trend_analysis = {}
        for year in aggregated_data["years"]:
            real_values = [
                safe_float(month["value"])
                for month in aggregated_data["aggregatedAverageReals"][year]
            ]
            real_values = [v for v in real_values if v is not None]

            yoy_growth = None
            if year > aggregated_data["years"][0]:
                prev_year_values = [
                    safe_float(month["value"])
                    for month in aggregated_data["aggregatedAverageReals"][year - 1]
                ]
                prev_year_values = [
                    v for v in prev_year_values if v is not None]
                if prev_year_values and sum(prev_year_values) != 0:
                    yoy_growth = safe_float(
                        (sum(real_values) - sum(prev_year_values))
                        / sum(prev_year_values)
                    )

            quarterly_growth = []
            for i in range(1, 4):
                current_quarter = sum(real_values[i * 3: (i + 1) * 3])
                previous_quarter = sum(real_values[(i - 1) * 3: i * 3])
                if previous_quarter != 0:
                    qoq_growth = safe_float(
                        (current_quarter - previous_quarter) / previous_quarter
                    )
                    quarterly_growth.append(qoq_growth)
                else:
                    quarterly_growth.append(None)

            trend_analysis[year] = {
                "year_over_year_growth": yoy_growth,
                "quarter_over_quarter_growth": quarterly_growth,
            }

        return trend_analysis

    @staticmethod
    def _estimate_market_share(enterprise_id, aggregated_data, description):
        enterprise_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, description=description
        )
        market_share = {}
        for year in aggregated_data["years"]:
            enterprise_revenue = sum(
                safe_float(revenue.real_income) or 0
                for revenue in enterprise_data.filter(year=str(year))
            )
            industry_revenue = sum(
                safe_float(month["value"]) or 0
                for month in aggregated_data["aggregatedAverageReals"][year]
            )

            if industry_revenue > 0:
                market_share[year] = safe_float(
                    enterprise_revenue / industry_revenue)
            else:
                market_share[year] = None

        return market_share

    @staticmethod
    def _adjust_budgets(enterprise_id, aggregated_data, pca_coefficients, description):
        enterprise_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, description=description
        )
        adjusted_budgets = {}

        for year in aggregated_data["years"]:
            annual_budget = sum(
                safe_float(revenue.expected_income) or 0
                for revenue in enterprise_data.filter(year=str(year))
            )

            if annual_budget > 0 and pca_coefficients:
                monthly_adjusted_budgets = []
                sum_abs_coef = sum(abs(c)
                                   for c in pca_coefficients if c is not None)
                if sum_abs_coef > 0:
                    for i, coef in enumerate(pca_coefficients):
                        if coef is not None:
                            adjusted_budget = safe_float(
                                (annual_budget * abs(coef)) / sum_abs_coef
                            )
                            monthly_adjusted_budgets.append(
                                {"month": i + 1, "adjusted_budget": adjusted_budget}
                            )
                    adjusted_budgets[year] = monthly_adjusted_budgets
                else:
                    adjusted_budgets[year] = None
            else:
                adjusted_budgets[year] = None

        return adjusted_budgets
