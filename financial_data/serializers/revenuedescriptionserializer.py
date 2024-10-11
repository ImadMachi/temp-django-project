from rest_framework import serializers
from ..models import *


class RevenueDescriptionSerializer(serializers.Serializer):
    enterprise = serializers.IntegerField()
    description = serializers.CharField(allow_null=True, allow_blank=True)
    revenue_id = serializers.IntegerField()
