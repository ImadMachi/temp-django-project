from financial_data.models import Revenue, YearIncomeDetail, MonthIncomeDetail
from rest_framework import serializers

from financial_data.serializers.incomeDetailSerializer import IncomeDetailSerializer


class BulkIncomeDetailSerializer(serializers.Serializer):
    income_details = IncomeDetailSerializer(many=True)

    def create(self, validated_data):
        income_details = validated_data["income_details"]
        for income_detail in income_details:
            serializer = IncomeDetailSerializer(data=income_detail)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return validated_data
