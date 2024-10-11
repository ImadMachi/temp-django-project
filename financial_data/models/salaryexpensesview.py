from django.db import models
from .enterprise import Enterprise


class SalaryExpensesView(models.Model):
    enterprise = models.ForeignKey(
        Enterprise, models.DO_NOTHING, db_column="EnterpriseId", primary_key=True
    )
    financial_detail_id = models.BigIntegerField(db_column="FinancialDetailId")
    employee_id = models.BigIntegerField(db_column="EmployeeId")
    first_name = models.TextField(db_column="FirstName")
    name = models.TextField(db_column="Name")
    year = models.TextField(db_column="Year")
    budget_total = models.DecimalField(
        db_column="BudgetTotal", max_digits=65, decimal_places=30
    )
    real_total = models.DecimalField(
        db_column="RealTotal", max_digits=65, decimal_places=30
    )
    total_performance = models.DecimalField(
        db_column="TotalPerformance", max_digits=65, decimal_places=30
    )
    month = models.IntegerField(db_column="Month")
    budget = models.DecimalField(db_column="Budget", max_digits=18, decimal_places=2)
    real = models.DecimalField(db_column="Real", max_digits=18, decimal_places=2)
    performance = models.DecimalField(
        db_column="Performance", max_digits=18, decimal_places=2
    )

    class Meta:
        managed = False
        db_table = "salaryexpensesview"
        unique_together = (
            ("enterprise", "financial_detail_id", "employee_id", "year", "month"),
        )

    def __str__(self):
        return f"{self.enterprise} - {self.employee_id} - {self.year} - {self.month}"
