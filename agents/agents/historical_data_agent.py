from django.db.models import Sum
from financial_data.models import (
    RevenuesView,
    OpportunityBookView,
    OrderBookView,
    SalesBudgetsView,
    EnterpriseIndustryView,
)
from .validation_agent import ValidationAgent
from django.utils import timezone


class HistoricalDataAgent:
    @staticmethod
    def execute(enterprise_id, description=None, current_year=None):
        if current_year is None:
            current_year = timezone.now().year

        # Check if the enterprise exists
        if not EnterpriseIndustryView.objects.filter(
            enterprise_id=enterprise_id
        ).exists():
            return {
                "error": f"Enterprise with ID {enterprise_id} does not exist.",
                "data_validity": None,
                "historical_data": {},
            }

        # Run the ValidationAgent to check data validity
        validation_result = ValidationAgent.execute(enterprise_id)

        # Check if ValidationAgent returned an error
        if "error" in validation_result:
            return validation_result

        result = {
            "data_validity": validation_result["validations"],
            "historical_data": {},
        }

        # Process and include monthly data for revenue if valid or monthly
        if validation_result["validations"].get("revenue", False) or validation_result[
            "validations"
        ].get("monthly_revenue", False):
            result["historical_data"]["Revenues Real History"] = (
                HistoricalDataAgent._get_revenue_history(
                    enterprise_id, description, current_year
                )
            )

        # Process and include monthly data for sales budget if valid or monthly
        if validation_result["validations"].get(
            "sales_budget", False
        ) or validation_result["validations"].get("monthly_sales_budget", False):
            result["historical_data"]["Sales Budget history"] = (
                HistoricalDataAgent._get_sales_budget_history(
                    enterprise_id, description, current_year
                )
            )

        # Process and include monthly data for performance if valid or monthly
        if validation_result["validations"].get(
            "performance", False
        ) or validation_result["validations"].get("monthly_performance", False):
            result["historical_data"]["Revenues Performance History"] = (
                HistoricalDataAgent._get_performance_history(
                    enterprise_id, description, current_year
                )
            )

        return result

    @staticmethod
    def _get_revenue_history(enterprise_id, description, current_year):
        revenues = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, year__lte=current_year
        )
        if description:
            revenues = revenues.filter(description=description)
        return list(
            revenues.values("year", "month", "description")
            .annotate(
                real=Sum("real_income"),
                budget=Sum("expected_total_income"),
            )
            .order_by("year", "month")
        )

    @staticmethod
    def _get_sales_budget_history(enterprise_id, description, current_year):
        sales_budgets = SalesBudgetsView.objects.filter(
            enterprise_id=enterprise_id, year__lte=current_year
        )
        if description:
            sales_budgets = sales_budgets.filter(description=description)
        return list(
            sales_budgets.values("year", "month", "description")
            .annotate(budget=Sum("budget"), real=Sum("real"))
            .order_by("year", "month")
        )

    @staticmethod
    def _get_performance_history(enterprise_id, description, current_year):
        performance = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, year__lte=current_year
        )
        if description:
            performance = performance.filter(description=description)
        return list(
            performance.values("year", "month", "description")
            .annotate(performance=Sum("total_income_performance"))
            .order_by("year", "month")
        )
