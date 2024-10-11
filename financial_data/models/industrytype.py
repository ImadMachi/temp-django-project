from django.db import models

class IndustryType(models.Model):
    label = models.CharField(db_column="Label", max_length=95)
    active = models.BooleanField(db_column="Active")

    class Meta:
        managed = True
        db_table = "industry_types"

    def __str__(self):
        return self.label



