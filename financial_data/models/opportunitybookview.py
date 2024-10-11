from django.db import models
from .enterprise import Enterprise

class OpportunityBookView(models.Model):
    enterprise = models.ForeignKey(
        Enterprise, models.DO_NOTHING, db_column="EnterpriseId", primary_key=True
    )
    year = models.TextField(db_column="Year", blank=True, null=True)
    total_opportunity_value = models.DecimalField(
        db_column="TotalOpportunityValue",
        max_digits=65,
        decimal_places=30,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "opportunity_book_view"
        unique_together = (("enterprise", "year"),)

    def __str__(self):
        return f"{self.enterprise} - {self.year}"



