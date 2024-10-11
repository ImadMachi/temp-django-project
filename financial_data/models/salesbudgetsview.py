from django.db import models
from .enterprise import Enterprise


class SalesBudgetsView(models.Model):
    enterprise = models.ForeignKey(
        Enterprise, models.DO_NOTHING, db_column="EnterpriseId", primary_key=True
    )
    revenue_id = models.BigIntegerField(db_column="RevenueId")
    sales_budget_id = models.BigIntegerField(db_column="SalesBudgetId")
    description = models.TextField(db_column="Description", blank=True, null=True)
    year = models.TextField(db_column="Year", blank=True, null=True)
    selling_price = models.DecimalField(
        db_column="SellingPrice", max_digits=65, decimal_places=30
    )
    sold_units_budget_total = models.FloatField(db_column="SoldUnitsBudgetTotal")
    sold_units_real_total = models.FloatField(db_column="SoldUnitsRealTotal")
    sold_units_performance_total = models.FloatField(
        db_column="SoldUnitsPerformanceTotal"
    )
    budget_total = models.DecimalField(
        db_column="BudgetTotal", max_digits=65, decimal_places=30
    )
    real_total = models.DecimalField(
        db_column="RealTotal", max_digits=65, decimal_places=30
    )
    performance_total = models.DecimalField(
        db_column="PerformanceTotal", max_digits=65, decimal_places=30
    )
    month = models.IntegerField(db_column="Month")
    sold_units_budget = models.FloatField(db_column="SoldUnitsBudget")
    real_sold_units = models.FloatField(db_column="RealSoldUnits")
    sold_units_performance = models.FloatField(db_column="SoldUnitsPerformance")
    budget = models.DecimalField(db_column="Budget", max_digits=65, decimal_places=30)
    real = models.DecimalField(db_column="Real", max_digits=65, decimal_places=30)
    performance = models.DecimalField(
        db_column="Performance", max_digits=65, decimal_places=30
    )

    class Meta:
        managed = False
        db_table = "salesbudgetsview"
        unique_together = (
            ("enterprise", "revenue_id", "sales_budget_id", "year", "month"),
        )

    def __str__(self):
        return (
            f"{self.enterprise} - {self.sales_budget_id} - {self.year} - {self.month}"
        )
