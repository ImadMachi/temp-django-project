import pandas as pd
import numpy as np
from django.db.models import Sum
from financial_data.models import RevenuesView, EnterpriseIndustryView, Enterprise
from decimal import Decimal
import matplotlib.pyplot as plt
import traceback
from .validation_agent import ValidationAgent
import json
from urllib.parse import unquote
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PredGlobaleAgent:
    @staticmethod
    def execute(enterprise_id, description=None, growth_rate=0.05):
        try:
            # First, check if the enterprise exists and get its name
            enterprise = Enterprise.objects.filter(id=enterprise_id).first()
            if not enterprise:
                logger.error(f"Enterprise with ID {
                             enterprise_id} does not exist.")
                return {
                    "error": f"Enterprise with ID {enterprise_id} does not exist.",
                    "data_validity": None,
                }

            enterprise_name = enterprise.name

            # Validate the enterprise data first
            validation_result = ValidationAgent.execute(enterprise_id)

            if not validation_result["validations"]["revenue"]:
                logger.error(
                    f"Insufficient revenue data for analysis for enterprise {
                        enterprise_id}"
                )
                return {
                    "error": "Insufficient revenue data for analysis",
                    "data_validity": validation_result["validations"],
                }

            # Set the prediction year to next year
            prediction_year = datetime.now().year + 1
            current_year = prediction_year - 1
            last_year = current_year - 1

            # Fetch historical revenue data
            revenues = RevenuesView.objects.filter(enterprise_id=enterprise_id)
            logger.info(
                f"Found {revenues.count()} revenue records for enterprise {
                    enterprise_id}"
            )
            print(f"Found {revenues[0]} revenue records for enterprise {
                  enterprise_id}")

            # If a description is provided, filter the revenues by that description
            if description:
                description = unquote(description.strip('"'))
                revenues = revenues.filter(description__iexact=description)
                logger.info(
                    f"Filtered to {revenues.count()} records for description '{
                        description}'"
                )

            if not revenues.exists():
                logger.error(
                    f"No revenue data found for enterprise_id {
                        enterprise_id} and description '{description}'"
                )
                return {
                    "error": f"No revenue data found for enterprise_id {enterprise_id} and description '{description}'",
                    "data_validity": validation_result["validations"],
                }

            # Log available descriptions
            available_descriptions = revenues.values_list(
                "description", flat=True
            ).distinct()
            logger.info(
                f"Available descriptions for enterprise {
                    enterprise_id}: {list(available_descriptions)}"
            )

            data = pd.DataFrame(
                list(revenues.values("year", "month", "real_income", "description"))
            )

            # Ensure 'year' is an integer and 'real_income' is float
            data["year"] = pd.to_numeric(
                data["year"], errors="coerce").astype("Int64")
            data["real_income"] = pd.to_numeric(
                data["real_income"], errors="coerce")

            # Drop rows with NaN values
            data = data.dropna()

            if data.empty:
                logger.error(
                    f"No valid data available after cleaning for enterprise {
                        enterprise_id}"
                )
                return {
                    "error": "No valid data available after cleaning",
                    "data_validity": validation_result["validations"],
                }

            # Rename columns to match the original code
            data = data.rename(
                columns={
                    "year": "Year",
                    "month": "Month",
                    "real_income": "RealIncome",
                    "description": "Description",
                }
            )

            # Group data by Year, Month, and Description, summing up the RealIncome for each group
            monthly_income = (
                data.groupby(["Year", "Month", "Description"])["RealIncome"]
                .sum()
                .unstack(level=["Month", "Description"])
            )

            # Filter the data for years before the prediction year
            data_before_prediction = monthly_income[
                monthly_income.index < prediction_year
            ]

            if data_before_prediction.empty:
                logger.error(
                    f"No historical data available for prediction for enterprise {
                        enterprise_id}"
                )
                return {
                    "error": "No historical data available for prediction",
                    "data_validity": validation_result["validations"],
                }

            results = {}

            for desc in data_before_prediction.columns.get_level_values(
                "Description"
            ).unique():
                description_data = data_before_prediction.xs(
                    desc, axis=1, level="Description"
                )

                if len(description_data) >= 2:
                    current_year_data = description_data.iloc[-1]
                    previous_year_data = description_data.iloc[-2]

                    # If current year is all zeros, use previous year as base
                    if (current_year_data == 0).all():
                        base_prediction = previous_year_data
                    else:
                        base_prediction = current_year_data

                    # Apply growth rate
                    predicted_distribution = base_prediction * \
                        (1 + growth_rate)

                else:
                    # Not enough historical data, use the only available year with growth
                    predicted_distribution = description_data.iloc[-1] * (
                        1 + growth_rate
                    )

                # Round and convert to int
                predicted_distribution = predicted_distribution.round().astype(int)

                results[desc] = {
                    str(prediction_year): predicted_distribution.to_dict(),
                    str(current_year): (
                        description_data.iloc[-1].to_dict()
                        if not description_data.empty
                        else None
                    ),
                    str(last_year): (
                        description_data.iloc[-2].to_dict()
                        if len(description_data) > 1
                        else None
                    ),
                }

            logger.info(f"Prediction completed for enterprise {enterprise_id}")
            return {
                "enterprise_id": enterprise_id,
                "enterprise_name": enterprise_name,
                "prediction_year": prediction_year,
                "results": results,
                "data_validity": validation_result["validations"],
                "growth_rate": growth_rate,
            }

        except Exception as e:
            logger.error(
                f"Unexpected error in PredGlobaleAgent.execute: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "error": f"An unexpected error occurred: {str(e)}",
                "traceback": traceback.format_exc(),
                "data_validity": (
                    validation_result["validations"]
                    if "validation_result" in locals()
                    else None
                ),
            }

    @staticmethod
    def plot_prediction(result):
        if "error" in result:
            print(f"Error: {result['error']}")
            return

        for description, data in result["results"].items():
            plt.figure(figsize=(14, 7))

            prediction_year = result["prediction_year"]
            predicted_data = pd.Series(data[str(prediction_year)])
            current_year_data = (
                pd.Series(data[str(prediction_year - 1)])
                if data[str(prediction_year - 1)]
                else None
            )
            last_year_data = (
                pd.Series(data[str(prediction_year - 2)])
                if data[str(prediction_year - 2)]
                else None
            )

            if last_year_data is not None and not last_year_data.empty:
                plt.plot(
                    last_year_data.index,
                    last_year_data.values,
                    label=f"{prediction_year - 2}",
                    marker="o",
                )

            if current_year_data is not None and not current_year_data.empty:
                plt.plot(
                    current_year_data.index,
                    current_year_data.values,
                    label=f"{prediction_year - 1}",
                    marker="o",
                )

            plt.plot(
                predicted_data.index,
                predicted_data.values,
                label=f"Predicted {prediction_year}",
                marker="o",
                linestyle="--",
            )

            plt.title(
                f'Monthly Income Distribution for Enterprise {
                    result["enterprise_id"]} ({result["enterprise_name"]})\nRevenue Type: {description}'
            )
            plt.xlabel("Month")
            plt.ylabel("Income")
            plt.xticks(range(1, 13))
            plt.legend()
            plt.grid(True)
            plt.show()

        print(
            f"\nNote: These predictions are for the year {
                result['prediction_year']}, based on historical data"
        )
        print(f"and using a growth rate of {result['growth_rate']*100}%")
