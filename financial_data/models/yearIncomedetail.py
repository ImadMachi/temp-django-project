from django.db import models
from .revenue import Revenue


class YearIncomeDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=4)
    expectedTotalUnits = models.FloatField(null=True, blank=True)
    expectedTotalIncome = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    realTotalUnits = models.FloatField(null=True, blank=True)
    realTotalIncome = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    totalUnitsPerformance = models.FloatField(null=True, blank=True)
    totalIncomePerformance = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    sellingPrice = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    RevenueId = models.ForeignKey(
        Revenue, on_delete=models.CASCADE, db_column="RevenueId"
    )

    class Meta:
        db_table = "incomedetail"
        managed = False
