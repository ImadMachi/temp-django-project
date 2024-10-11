from django.db import models
from .enterprise import Enterprise


class RevenuesView(models.Model):
    enterprise = models.ForeignKey(
        Enterprise, models.DO_NOTHING, db_column="EnterpriseId", primary_key=True
    )
    revenue_id = models.BigIntegerField(db_column="RevenueId")
    description = models.TextField(db_column="Description", blank=True, null=True)
    gifi = models.CharField(db_column="GIFI", max_length=95, blank=True, null=True)
    year = models.TextField(db_column="Year", blank=True, null=True)
    selling_price = models.DecimalField(
        db_column="SellingPrice", max_digits=65, decimal_places=30
    )
    expected_total_units = models.FloatField(db_column="ExpectedTotal Units")
    real_total_units = models.FloatField(db_column="RealTotalUnits")
    total_units_performance = models.FloatField(db_column="TotalUnitsPerformance")
    expected_total_income = models.DecimalField(
        db_column="ExpectedTotalIncome", max_digits=65, decimal_places=30
    )
    real_total_income = models.DecimalField(
        db_column="RealTotalIncome", max_digits=65, decimal_places=30
    )
    total_income_performance = models.DecimalField(
        db_column="TotalIncomePerformance", max_digits=65, decimal_places=30
    )
    month = models.IntegerField(db_column="Month")
    expected_sold_units = models.FloatField(db_column="ExpectedSoldUnits")
    real_sold_units = models.FloatField(db_column="RealSoldUnits")
    sold_units_performance = models.FloatField(db_column="SoldUnitsPerformance")
    expected_income = models.DecimalField(
        db_column="ExpectedIncome", max_digits=65, decimal_places=30
    )
    real_income = models.DecimalField(
        db_column="RealIncome", max_digits=65, decimal_places=30
    )
    income_performance = models.DecimalField(
        db_column="IncomePerformance", max_digits=65, decimal_places=30
    )

    class Meta:
        managed = False
        db_table = "revenuesview"
        unique_together = (("enterprise", "revenue_id", "year", "month"),)

    def __str__(self):
        return f"{self.enterprise} - {self.revenue_id} - {self.year} - {self.month}"
