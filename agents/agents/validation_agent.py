from django.db.models import Count, Avg, Sum, F, ExpressionWrapper, fields, StdDev
from financial_data.models import (
    RevenuesView,
    SalesBudgetsView,
    OrderBookView,
    OpportunityBookView,
    EnterpriseIndustryView,
)
from datetime import datetime
from decimal import Decimal, InvalidOperation


class ValidationAgent:

    @staticmethod
    def execute(enterprise_id):
        # Check if the enterprise exists
        if not EnterpriseIndustryView.objects.filter(
            enterprise_id=enterprise_id
        ).exists():
            return {
                "error": f"Enterprise with ID {enterprise_id} does not exist.",
                "enterprise_id": enterprise_id,
                "validations": {},
                "data_quality": {},
                "overall_validation": False,
                "recommendations": [
                    "Enterprise does not exist. Please check the enterprise ID."
                ],
            }

        result = {
            "enterprise_id": enterprise_id,
            "validations": {},
            "data_quality": {},
            "overall_validation": True,
            "recommendations": [],
        }

        current_year = datetime.now().year
        five_years_ago = str(current_year - 5)

        # Check Revenue Data
        revenue_data = ValidationAgent._analyze_revenue_data(
            enterprise_id, five_years_ago
        )
        result["validations"]["revenue"] = revenue_data["valid"]
        result["data_quality"]["revenue"] = revenue_data["quality"]

        # Check if revenue is recurrent
        recurrent_revenue = ValidationAgent._check_recurrent_revenue(
            enterprise_id, five_years_ago
        )
        result["validations"]["recurrent_revenue"] = recurrent_revenue["is_recurrent"]
        result["data_quality"]["recurrent_revenue"] = recurrent_revenue[
            "recurrence_score"
        ]

        # Check Sales Budget Data
        sales_budget_data = ValidationAgent._analyze_sales_budget_data(
            enterprise_id, five_years_ago
        )
        result["validations"]["sales_budget"] = sales_budget_data["valid"]
        result["data_quality"]["sales_budget"] = sales_budget_data["quality"]

        # Check Order Book Data
        order_book_data = ValidationAgent._analyze_order_book_data(
            enterprise_id, five_years_ago
        )
        result["validations"]["order_book"] = order_book_data["valid"]
        result["data_quality"]["order_book"] = order_book_data["quality"]

        # Check Opportunity Data
        opportunity_data = ValidationAgent._analyze_opportunity_data(
            enterprise_id, five_years_ago
        )
        result["validations"]["opportunity"] = opportunity_data["valid"]
        result["data_quality"]["opportunity"] = opportunity_data["quality"]

        # Check Performance Data
        performance_data = ValidationAgent._analyze_performance_data(
            enterprise_id, five_years_ago
        )
        result["validations"]["performance"] = performance_data["valid"]
        result["data_quality"]["performance"] = performance_data["quality"]

        # Check for monthly data
        result["validations"]["monthly_revenue"] = ValidationAgent._check_monthly_data(
            RevenuesView, enterprise_id, five_years_ago
        )
        result["validations"]["monthly_sales_budget"] = (
            ValidationAgent._check_monthly_data(
                SalesBudgetsView, enterprise_id, five_years_ago
            )
        )
        result["validations"]["monthly_order_book"] = (
            ValidationAgent._check_monthly_data(
                OrderBookView, enterprise_id, five_years_ago
            )
        )
        result["validations"]["monthly_opportunity"] = (
            ValidationAgent._check_monthly_data(
                OpportunityBookView, enterprise_id, five_years_ago
            )
        )
        result["validations"]["monthly_performance"] = (
            ValidationAgent._check_monthly_performance(enterprise_id, five_years_ago)
        )

        # Overall validation
        result["overall_validation"] = all(result["validations"].values())

        # Generate recommendations
        ValidationAgent._generate_recommendations(result)
        return result

    @staticmethod
    def _analyze_revenue_data(enterprise_id, five_years_ago):
        revenue_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )
        years_count = revenue_data.values("year").distinct().count()
        months_count = revenue_data.values("year", "month").distinct().count()
        yearly_revenue = (
            revenue_data.values("year")
            .annotate(
                total_revenue=Sum("real_income")
            )  # Changed from real_total_income to real_income
            .order_by("year")
        )
        avg_yearly_growth = ValidationAgent._calculate_avg_growth(
            yearly_revenue, "total_revenue"
        )
        return {
            "valid": years_count > 1,
            "quality": {
                "years_available": years_count,
                "months_available": months_count,
                "avg_yearly_growth": avg_yearly_growth,
                "data_consistency": ValidationAgent._check_data_consistency(
                    yearly_revenue, "total_revenue"
                ),
            },
        }

    @staticmethod
    def _analyze_performance_data(enterprise_id, five_years_ago):
        performance_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )
        years_count = performance_data.values("year").distinct().count()
        avg_performance = (
            performance_data.aggregate(Avg("income_performance"))[
                "income_performance__avg"
            ]
            or 0
        )
        performance_consistency = ValidationAgent._check_data_consistency(
            performance_data.values("year").annotate(
                performance=Avg("income_performance")
            ),
            "performance",
        )
        return {
            "valid": years_count > 1,
            "quality": {
                "years_available": years_count,
                "avg_performance": avg_performance,
                "performance_consistency": performance_consistency,
            },
        }

    @staticmethod
    def _check_monthly_performance(enterprise_id, five_years_ago):
        performance_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )
        total_possible_months = (datetime.now().year - int(five_years_ago) + 1) * 12
        months_with_data = performance_data.values("year", "month").distinct().count()
        return (
            months_with_data / total_possible_months >= 0.5
        )  # Consider it monthly if at least 50% of months are present

    @staticmethod
    def _check_recurrent_revenue(enterprise_id, five_years_ago):
        revenue_data = RevenuesView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )

        if not revenue_data.exists():
            return {"is_recurrent": False, "recurrence_score": 0}

        monthly_stats = revenue_data.values("month").annotate(
            avg_revenue=Avg("real_income"),
            std_dev=StdDev(
                "real_income"
            ),  # Changed from real_total_income to real_income
        )

        if not monthly_stats:
            return {"is_recurrent": False, "recurrence_score": 0}

        cvs = []
        for stat in monthly_stats:
            if stat["avg_revenue"] and stat["avg_revenue"] > 0:
                cv = (
                    stat["std_dev"] / stat["avg_revenue"]
                    if stat["std_dev"] is not None
                    else 0
                )
                cvs.append(cv)

        if not cvs:
            return {"is_recurrent": False, "recurrence_score": 0}

        avg_cv = sum(cvs) / len(cvs)

        high_recurrence_threshold = 0.3
        medium_recurrence_threshold = 0.5

        if avg_cv <= high_recurrence_threshold:
            recurrence_score = 1.0
        elif avg_cv <= medium_recurrence_threshold:
            recurrence_score = 0.5
        else:
            recurrence_score = 0.0

        is_recurrent = recurrence_score > 0

        return {"is_recurrent": is_recurrent, "recurrence_score": recurrence_score}

    @staticmethod
    def _analyze_sales_budget_data(enterprise_id, five_years_ago):
        sales_budget_data = SalesBudgetsView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )
        sales_budget_data = sales_budget_data.exclude(budget=Decimal("0E-30")).exclude(
            real=Decimal("0E-30")
        )
        years_count = sales_budget_data.values("year").distinct().count()
        if years_count > 0:
            budget_accuracy = (
                sales_budget_data.aggregate(
                    accuracy=ExpressionWrapper(
                        Avg(F("real") / F("budget")), output_field=fields.FloatField()
                    )
                )["accuracy"]
                or 0
            )
        else:
            budget_accuracy = 0
        yearly_budget = sales_budget_data.values("year").annotate(total=Sum("budget"))
        return {
            "valid": years_count > 1,
            "quality": {
                "years_available": years_count,
                "budget_accuracy": budget_accuracy,
                "data_consistency": ValidationAgent._check_data_consistency(
                    yearly_budget, "total"
                ),
            },
        }

    @staticmethod
    def _analyze_order_book_data(enterprise_id, five_years_ago):
        order_book_data = OrderBookView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )
        years_count = order_book_data.values("year").distinct().count()
        avg_order_value = (
            order_book_data.aggregate(Avg("total_order_value"))[
                "total_order_value__avg"
            ]
            or 0
        )
        yearly_orders = order_book_data.values("year").annotate(
            total=Sum("total_order_value")
        )
        return {
            "valid": years_count > 1,
            "quality": {
                "years_available": years_count,
                "avg_order_value": avg_order_value,
                "data_consistency": ValidationAgent._check_data_consistency(
                    yearly_orders, "total"
                ),
            },
        }

    @staticmethod
    def _analyze_opportunity_data(enterprise_id, five_years_ago):
        opportunity_data = OpportunityBookView.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )
        years_count = opportunity_data.values("year").distinct().count()
        total_opportunities = (
            opportunity_data.aggregate(
                total_opportunities=Sum("total_opportunity_value")
            )["total_opportunities"]
            or 0
        )
        conversion_rate = (
            total_opportunities  # You can define how to calculate this if needed
        )
        yearly_opportunities = opportunity_data.values("year").annotate(
            total=Sum("total_opportunity_value")
        )
        return {
            "valid": years_count > 1,
            "quality": {
                "years_available": years_count,
                "conversion_rate": conversion_rate,
                "data_consistency": ValidationAgent._check_data_consistency(
                    yearly_opportunities, "total"
                ),
            },
        }

    @staticmethod
    def _check_monthly_data(model, enterprise_id, five_years_ago):
        monthly_data = model.objects.filter(
            enterprise_id=enterprise_id, year__gte=five_years_ago
        )

        # Check if the model has a 'month' field
        if "month" in [f.name for f in model._meta.get_fields()]:
            # Group by year and month, then count distinct combinations
            data_points = monthly_data.values("year", "month").distinct().count()
            total_possible_months = (datetime.now().year - int(five_years_ago) + 1) * 12
            return (
                data_points / total_possible_months >= 0.5
            )  # Consider it monthly if at least 50% of months are present
        else:
            # If there's no 'month' field, check for at least one entry per year
            years_with_data = monthly_data.values("year").distinct().count()
            total_years = datetime.now().year - int(five_years_ago) + 1
            return (
                years_with_data / total_years >= 0.8
            )  # Consider it sufficient if data is present for at least 80% of years

    @staticmethod
    def _check_data_consistency(yearly_data, value_field):
        if len(yearly_data) < 2:
            return None
        variations = []
        for i, y in enumerate(yearly_data):
            if i > 0:
                prev_value = yearly_data[i - 1][value_field]
                current_value = y[value_field]
                if prev_value and prev_value != 0:
                    try:
                        variation = (current_value - prev_value) / prev_value
                        variations.append(float(variation))
                    except (InvalidOperation, TypeError, ZeroDivisionError):
                        continue
        if not variations:
            return None
        avg_variation = sum(variations) / len(variations)
        return 1 - abs(avg_variation)  # Higher value means more consistent data

    @staticmethod
    def _calculate_avg_growth(yearly_data, value_field):
        if len(yearly_data) < 2:
            return None
        growths = []
        for i, y in enumerate(yearly_data):
            if i > 0:
                prev_value = yearly_data[i - 1][value_field]
                current_value = y[value_field]
                if prev_value and prev_value != 0:
                    try:
                        growth = (current_value - prev_value) / prev_value
                        growths.append(float(growth))
                    except (InvalidOperation, TypeError, ZeroDivisionError):
                        continue
        return sum(growths) / len(growths) if growths else None

    @staticmethod
    def _generate_recommendations(result):
        if not result["overall_validation"]:
            if not result["validations"]["revenue"]:
                result["recommendations"].append(
                    "Insufficient historical revenue data. Expand data collection to improve analysis accuracy."
                )
            if not result["validations"]["sales_budget"]:
                result["recommendations"].append(
                    "Limited sales budget history. Consider incorporating more historical budget data for better forecasting."
                )
            if not result["validations"]["order_book"]:
                result["recommendations"].append(
                    "Insufficient order book history. Enhance order tracking to improve future predictions."
                )
            if not result["validations"]["opportunity"]:
                result["recommendations"].append(
                    "Limited opportunity data. Implement robust opportunity tracking to refine sales forecasts."
                )
            if not result["validations"]["performance"]:
                result["recommendations"].append(
                    "Insufficient performance data. Ensure consistent tracking of performance metrics for better analysis."
                )

        for data_type, quality in result["data_quality"].items():
            if isinstance(quality, dict) and "data_consistency" in quality:
                if quality["data_consistency"] is not None:
                    if quality["data_consistency"] < 0.3:
                        result["recommendations"].append(
                            f"Very low consistency detected in {data_type} data. Urgently review and improve data collection processes."
                        )
                    elif quality["data_consistency"] < 0.5:
                        result["recommendations"].append(
                            f"Low consistency detected in {data_type} data. Review data collection processes for potential improvements."
                        )
                    elif quality["data_consistency"] < 0.7:
                        result["recommendations"].append(
                            f"Moderate consistency in {data_type} data. Consider ways to further improve data reliability."
                        )

        if "sales_budget" in result["data_quality"]:
            budget_accuracy = result["data_quality"]["sales_budget"].get(
                "budget_accuracy"
            )
            if budget_accuracy is not None:
                if budget_accuracy < 0.5:
                    result["recommendations"].append(
                        "Very low budget accuracy detected. Urgently review budgeting process to improve alignment with actual results."
                    )
                elif budget_accuracy < 0.8:
                    result["recommendations"].append(
                        "Low budget accuracy detected. Review budgeting process to improve alignment with actual results."
                    )
                elif budget_accuracy < 0.9:
                    result["recommendations"].append(
                        "Moderate budget accuracy. Consider fine-tuning your budgeting process for even better forecasts."
                    )

        if result["validations"]["recurrent_revenue"]:
            recurrence_score = result["data_quality"]["recurrent_revenue"]
            if recurrence_score == 1.0:
                result["recommendations"].append(
                    "Revenue shows high recurrence. This predictability can be leveraged for more accurate forecasting and strategic planning."
                )
            elif recurrence_score == 0.5:
                result["recommendations"].append(
                    "Revenue shows moderate recurrence. Consider strategies to increase recurring revenue streams for improved predictability."
                )
        else:
            result["recommendations"].append(
                "Revenue does not show strong recurrence patterns. Explore opportunities to develop more predictable revenue streams and diversify income sources."
            )

        if result["validations"]["performance"]:
            avg_performance = result["data_quality"]["performance"]["avg_performance"]
            if avg_performance < 0.6:
                result["recommendations"].append(
                    f"Average performance ({avg_performance:.2f}) is significantly below target. Urgently review strategies and implement improvement plans."
                )
            elif avg_performance < 0.8:
                result["recommendations"].append(
                    f"Average performance ({avg_performance:.2f}) is below target. Review strategies to improve overall performance."
                )
            elif avg_performance > 1.2:
                result["recommendations"].append(
                    f"Average performance ({avg_performance:.2f}) is significantly above target. Consider adjusting targets, expanding operations, or reinvesting in growth."
                )
            else:
                result["recommendations"].append(
                    f"Average performance ({avg_performance:.2f}) is within expected range. Continue monitoring and optimizing strategies for sustained success."
                )
        else:
            result["recommendations"].append(
                "Insufficient performance data available. Implement consistent performance tracking for better insights and decision-making."
            )

        if result["validations"]["monthly_performance"]:
            result["recommendations"].append(
                "Monthly performance data is available, which allows for more detailed trend analysis and forecasting. Utilize this granular data for more precise planning."
            )
        else:
            result["recommendations"].append(
                "Monthly performance data is incomplete. Implement more frequent performance tracking for improved insights and ability to react quickly to changes."
            )

        monthly_data_types = [
            "revenue",
            "sales_budget",
            "order_book",
            "opportunity",
            "performance",
        ]
        missing_monthly_data = [
            data_type
            for data_type in monthly_data_types
            if not result["validations"][f"monthly_{data_type}"]
        ]
        if missing_monthly_data:
            result["recommendations"].append(
                f"Monthly data is missing or incomplete for: {', '.join(missing_monthly_data)}. Implement monthly tracking for these areas to improve prediction accuracy and enable more timely decision-making."
            )
        else:
            result["recommendations"].append(
                "Excellent! Monthly data is available for all key areas. Leverage this comprehensive data for detailed analysis, accurate forecasting, and agile business strategies."
            )

        if not result["recommendations"]:
            result["recommendations"].append(
                "Data quality is sufficient for analysis. Continue maintaining consistent data collection practices and consider more advanced analytics to gain deeper insights."
            )

        return result
