from rest_framework import serializers
from financial_data.models.yearIncomedetail import YearIncomeDetail
from financial_data.models.revenue import Revenue
from financial_data.models.monthIncomeDetail import MonthIncomeDetail


class IncomeDetailSerializer(serializers.Serializer):
    enterpriseId = serializers.IntegerField()
    revenueId = serializers.CharField()
    category = serializers.CharField()
    predictionYear = serializers.IntegerField()
    month1 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month2 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month3 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month4 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month5 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month6 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month7 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month8 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month9 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month10 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month11 = serializers.DecimalField(max_digits=65, decimal_places=30)
    month12 = serializers.DecimalField(max_digits=65, decimal_places=30)
    total = serializers.DecimalField(max_digits=65, decimal_places=30)

    def create(self, validated_data):
        revenue_id = validated_data["revenueId"]
        enterprise_id = validated_data["enterpriseId"]
        year = str(validated_data["predictionYear"])

        revenue = Revenue.objects.get(id=revenue_id, EnterpriseId=enterprise_id)

        year_income_detail, created = YearIncomeDetail.objects.update_or_create(
            year=year,
            RevenueId=revenue,
            defaults={
                "expectedTotalIncome": validated_data["total"],
                "sellingPrice": revenue.sellingPrice,
                "expectedTotalUnits": sum(
                    validated_data[f"month{i}"] for i in range(1, 13)
                ),
            },
        )

        for i in range(1, 13):
            MonthIncomeDetail.objects.update_or_create(
                incomeDetailId=year_income_detail,
                month=i,
                defaults={
                    "expectedIncome": validated_data[f"month{i}"],
                    "sellingPrice": revenue.sellingPrice,
                    "expectedSoldUnits": validated_data[f"month{i}"],
                },
            )

        return validated_data
