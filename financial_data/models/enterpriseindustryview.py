from django.db import models

class EnterpriseIndustryView(models.Model):
    enterprise_id = models.BigIntegerField(primary_key=True, db_column="EnterpriseId")
    enterprise_name = models.TextField(db_column="EnterpriseName")
    business_number = models.TextField(db_column="BusinessNumber")
    budget_range = models.IntegerField(db_column="BudgetRange")
    founding_date = models.DateTimeField(db_column="FoundingDate")
    starting_date = models.DateTimeField(db_column="StartingDate")
    end_date = models.DateTimeField(db_column="EndDate", null=True)
    start_year = models.TextField(db_column="StartYear", null=True)
    start_period = models.IntegerField(db_column="StartPeriod")
    years_interval = models.PositiveSmallIntegerField(
        db_column="YearsInterval", null=True
    )
    employees_count = models.IntegerField(db_column="EmployeesCount", null=True)
    address = models.TextField(db_column="Address", null=True)
    postal_code = models.TextField(db_column="PostalCode", null=True)
    city_id = models.IntegerField(db_column="CityId", null=True)
    integrator_id = models.BigIntegerField(db_column="IntegratorId", null=True)
    current_plan_id = models.BigIntegerField(db_column="CurrentPlanId", null=True)
    taxes = models.DecimalField(
        db_column="Taxes", max_digits=5, decimal_places=2, null=True
    )
    supports_white_labeling = models.BooleanField(db_column="SupportsWhiteLabeling")
    logo_path = models.TextField(db_column="LogoPath", null=True)
    enterprise_active = models.BooleanField(db_column="EnterpriseActive")
    min_logo_path = models.TextField(db_column="MinLogoPath", null=True)
    industry_type_id = models.BigIntegerField(db_column="IndustryTypeId")
    industry_type_label = models.CharField(db_column="IndustryTypeLabel", max_length=95)
    industry_type_active = models.BooleanField(db_column="IndustryTypeActive")

    class Meta:
        managed = False
        db_table = "enterprise_industry_view"

    def __str__(self):
        return f"{self.enterprise_name} - {self.industry_type_label}"

