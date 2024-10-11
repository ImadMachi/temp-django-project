from django.db import models
from .yearIncomedetail import YearIncomeDetail


class MonthIncomeDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    realSoldUnits = models.FloatField(null=True, blank=True)
    realIncome = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    expectedSoldUnits = models.FloatField(null=True, blank=True)
    expectedIncome = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    soldUnitsPerformance = models.FloatField(null=True, blank=True)
    incomePerformance = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    sellingPrice = models.DecimalField(
        max_digits=65, decimal_places=30, null=True, blank=True
    )
    month = models.IntegerField()
    incomeDetailId = models.ForeignKey(
        YearIncomeDetail, on_delete=models.CASCADE, db_column="incomeDetailId"
    )

    class Meta:
        db_table = "monthincomedetail"
        managed = False
