from django.db import models

class Enterprise(models.Model):
    id = models.BigAutoField(db_column="Id", primary_key=True)
    name = models.TextField(db_column="Name")
    business_number = models.TextField(db_column="BusinessNumber")
    budget_range = models.IntegerField(db_column="BudgetRange")
    founding_date = models.DateTimeField(db_column="FoundingDate")
    starting_date = models.DateTimeField(db_column="StartingDate")
    end_date = models.DateTimeField(db_column="EndDate", blank=True, null=True)
    start_year = models.TextField(db_column="StartYear", blank=True, null=True)
    start_period = models.IntegerField(db_column="StartPeriod")
    years_interval = models.PositiveIntegerField(
        db_column="YearsInterval", blank=True, null=True
    )
    employees_count = models.IntegerField(
        db_column="EmployeesCount", blank=True, null=True
    )
    address = models.TextField(db_column="Address", blank=True, null=True)
    postal_code = models.TextField(db_column="PostalCode", blank=True, null=True)
    city_id = models.IntegerField(db_column="CityId", blank=True, null=True)
    integrator_id = models.BigIntegerField(
        db_column="IntegratorId", blank=True, null=True
    )
    current_plan_id = models.BigIntegerField(
        db_column="CurrentPlanId", blank=True, null=True
    )
    taxes = models.DecimalField(
        db_column="Taxes", max_digits=5, decimal_places=2, blank=True, null=True
    )
    supports_white_labeling = models.BooleanField(db_column="SupportsWhiteLabeling")
    logo_path = models.TextField(db_column="LogoPath", blank=True, null=True)
    active = models.BooleanField(db_column="Active")
    min_logo_path = models.TextField(db_column="MinLogoPath", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "enterprises"

    def __str__(self):
        return self.name



