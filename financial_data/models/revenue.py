from django.db import models


class Revenue(models.Model):
    sellingPrice = models.DecimalField(max_digits=65, decimal_places=30)
    commission = models.FloatField()
    hypothesis = models.TextField(null=True, blank=True)
    EnterpriseId = models.BigIntegerField(null=True, blank=True)
    EmployeeId = models.BigIntegerField(null=True, blank=True)
    ProductId = models.BigIntegerField(null=True, blank=True)
    SalesBudgetId = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "revenue"
