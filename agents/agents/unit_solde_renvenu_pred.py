import pandas as pd
from decimal import Decimal, getcontext
from financial_data.models import RevenuesView
from datetime import datetime

# Set the precision for Decimal calculations
getcontext().prec = 10


class UnitBasedRevenuePrediction:
    def __init__(self, enterprise_id, description, growth_rate=0.05):
        self.enterprise_id = enterprise_id
        self.description = description
        self.growth_rate = Decimal(str(growth_rate))
        self.current_year = datetime.now().year
        self.next_year = self.current_year + 1

    def fetch_data(self):
        data = (
            RevenuesView.objects.filter(
                enterprise_id=self.enterprise_id,
                description=self.description,
                year__lte=self.current_year,
            )
            .values("year", "month", "real_sold_units", "real_income")
            .order_by("year", "month")
        )
        return pd.DataFrame(data)

    def process_data(self):
        df = self.fetch_data()
        monthly_data = (
            df.groupby(["year", "month"])
            .agg({"real_sold_units": "sum", "real_income": "sum"})
            .reset_index()
        )
        monthly_data["unit_price"] = monthly_data.apply(
            lambda row: (
                Decimal(str(row["real_income"])) /
                Decimal(str(row["real_sold_units"]))
                if row["real_sold_units"] > 0
                else (
                    Decimal(str(row["real_income"]))
                    if row["real_income"] > 0
                    else Decimal("0")
                )
            ),
            axis=1,
        )
        return monthly_data

    def find_most_recent_year_with_data(self, data):
        yearly_data = data.groupby("year").agg(
            {"real_sold_units": "sum", "real_income": "sum"}
        )
        years_with_data = yearly_data[yearly_data["real_sold_units"] > 0].index
        return max(years_with_data) if len(years_with_data) > 0 else None

    def predict_next_year_revenue(self):
        monthly_data = self.process_data()
        base_year = self.find_most_recent_year_with_data(monthly_data)

        predicted_data = []

        if base_year is not None:
            base_year_data = monthly_data[monthly_data["year"] == base_year]
            for _, row in base_year_data.iterrows():
                if row["real_sold_units"] > 0:
                    predicted_units = int(
                        Decimal(str(row["real_sold_units"]))
                        * (Decimal("1") + self.growth_rate)
                    )
                    predicted_income = Decimal(
                        str(predicted_units)) * row["unit_price"]
                elif row["real_income"] > 0:
                    predicted_units = 0
                    predicted_income = Decimal(str(row["real_income"])) * (
                        Decimal("1") + self.growth_rate
                    )
                else:
                    predicted_units = 0
                    predicted_income = Decimal("0")

                predicted_data.append(
                    {
                        "year": self.next_year,
                        "month": row["month"],
                        "predicted_units": predicted_units,
                        "predicted_income": round(predicted_income, 2),
                        "predicted_unit_price": round(row["unit_price"], 2),
                    }
                )

        # If we have no data or incomplete data, fill in the missing months with zeros
        existing_months = set(item["month"] for item in predicted_data)
        for month in range(1, 13):
            if month not in existing_months:
                predicted_data.append(
                    {
                        "year": self.next_year,
                        "month": month,
                        "predicted_units": 0,
                        "predicted_income": Decimal("0"),
                        "predicted_unit_price": Decimal("0"),
                    }
                )

        # Sort the predictions by month
        predicted_data.sort(key=lambda x: x["month"])

        return predicted_data

    def predict_revenue_for_years(self, years):
        monthly_data = self.process_data()
        base_year = self.find_most_recent_year_with_data(monthly_data)
        all_predictions = []

        for year in range(self.next_year, self.next_year + years):
            year_predictions = []
            if base_year is not None:
                base_year_data = monthly_data[monthly_data["year"]
                                              == base_year]

                # growth factor
                year_growth = (Decimal("1") + self.growth_rate) ** Decimal(
                    str(year - base_year)
                )
                for _, row in base_year_data.iterrows():
                    if row["real_sold_units"] > 0:
                        predicted_units = int(
                            Decimal(str(row["real_sold_units"])) * year_growth
                        )
                        predicted_income = (
                            Decimal(str(predicted_units)) * row["unit_price"]
                        )
                    elif row["real_income"] > 0:
                        predicted_units = 0
                        predicted_income = (
                            Decimal(str(row["real_income"])) * year_growth
                        )
                    else:
                        predicted_units = 0
                        predicted_income = Decimal("0")

                    year_predictions.append(
                        {
                            "year": year,
                            "month": row["month"],
                            "predicted_units": predicted_units,
                            "predicted_income": round(predicted_income, 2),
                            "predicted_unit_price": round(row["unit_price"], 2),
                        }
                    )

            # Fill in any missing months with zeros
            existing_months = set(item["month"] for item in year_predictions)
            for month in range(1, 13):
                if month not in existing_months:
                    year_predictions.append(
                        {
                            "year": year,
                            "month": month,
                            "predicted_units": 0,
                            "predicted_income": Decimal("0"),
                            "predicted_unit_price": Decimal("0"),
                        }
                    )

            # Sort the predictions by month and add to all_predictions
            year_predictions.sort(key=lambda x: x["month"])
            all_predictions.extend(year_predictions)

        return all_predictions

    def get_summary(self, years=5):
        predictions = self.predict_revenue_for_years(years)
        df = pd.DataFrame(predictions)
        yearly_summary = (
            df.groupby("year")
            .agg(
                {
                    "predicted_units": "sum",
                    "predicted_income": "sum",
                    "predicted_unit_price": "mean",
                }
            )
            .reset_index()
        )
        yearly_summary["year_over_year_growth"] = yearly_summary[
            "predicted_income"
        ].pct_change()
        return yearly_summary.to_dict(orient="records")

    def get_prediction_data(self):
        monthly_data = self.process_data()
        historical_data = monthly_data.to_dict(orient="records")
        next_year_prediction = self.predict_next_year_revenue()

        total_predicted_units = sum(
            item["predicted_units"] for item in next_year_prediction
        )
        total_predicted_income = sum(
            Decimal(str(item["predicted_income"])) for item in next_year_prediction
        )

        if total_predicted_units > 0:
            avg_predicted_unit_price = total_predicted_income / Decimal(
                str(total_predicted_units)
            )
        else:
            avg_predicted_unit_price = Decimal("0")

        for item in historical_data:
            item["real_income"] = round(Decimal(str(item["real_income"])), 2)
            item["unit_price"] = round(Decimal(str(item["unit_price"])), 2)

        return {
            "enterprise_id": self.enterprise_id,
            "description": self.description,
            "growth_rate": float(self.growth_rate),
            "next_year": self.next_year,
            "historical_data": historical_data,
            "next_year_prediction": next_year_prediction,
            "prediction_summary": {
                "total_predicted_units": total_predicted_units,
                "total_predicted_income": round(total_predicted_income, 2),
                "average_predicted_unit_price": round(avg_predicted_unit_price, 2),
            },
        }
