from django.db import models


class OrderBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    enterprise = models.ForeignKey(
        "Enterprise", on_delete=models.CASCADE, db_column="EnterpriseiD"
    )
    name = models.TextField()
    created_at = models.DateTimeField(db_column="CreatedAt")
    year = models.IntegerField(null=True)
    total = models.DecimalField(max_digits=65, decimal_places=30, null=True)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "orderbooks"

    def __str__(self):
        return f"{self.enterprise.name} - {self.total} ({self.created_at})"
