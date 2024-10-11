from rest_framework import serializers
from financial_data.models.opportunitybook import OpportunityBook
from financial_data.serializers.enterpriseserializer import EnterpriseSerializer


class OpportunityBookSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseSerializer(read_only=True)

    class Meta:
        model = OpportunityBook
        fields = ["id", "enterprise", "name", "created_at", "year", "total", "active"]
