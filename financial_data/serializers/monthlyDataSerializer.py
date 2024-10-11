from financial_data.models import Revenue, YearIncomeDetail, MonthIncomeDetail
from rest_framework import serializers


class MonthlyDataSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    expectedIncome = serializers.DecimalField(max_digits=65, decimal_places=30)
