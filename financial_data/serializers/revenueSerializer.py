from rest_framework import serializers
from financial_data.models import Revenue, YearIncomeDetail, MonthIncomeDetail


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ["id", "sellingPrice", "commission", "EnterpriseId"]
