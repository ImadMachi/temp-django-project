from django.db import models
from .enterprise import Enterprise

class MarketingExpensesView(models.Model):
    enterprise = models.ForeignKey(
        Enterprise, models.DO_NOTHING, db_column="EnterpriseId", primary_key=True
    )
    marketing_id = models.BigIntegerField(db_column="MarketingId")
    year = models.TextField(db_column="Year", blank=True, null=True)
    budget_total = models.DecimalField(
        db_column="Budget Total", max_digits=65, decimal_places=30
    )
    real_total = models.DecimalField(
        db_column="Real Total", max_digits=65, decimal_places=30
    )
    total_performance = models.DecimalField(
        db_column="Total Performance", max_digits=65, decimal_places=30
    )
    month = models.IntegerField(db_column="Month")
    budget = models.DecimalField(db_column="Budget", max_digits=65, decimal_places=30)
    real = models.DecimalField(db_column="Real", max_digits=65, decimal_places=30)
    performance = models.DecimalField(
        db_column="Performance", max_digits=65, decimal_places=30
    )

    class Meta:
        managed = False
        db_table = "marketingexpensesview"
        unique_together = (("enterprise", "marketing_id", "year", "month"),)

    def __str__(self):
        return f"{self.enterprise} - {self.marketing_id} - {self.year} - {self.month}"



