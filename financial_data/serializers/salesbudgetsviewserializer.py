from rest_framework import serializers
from ..models import *

class SalesBudgetsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesBudgetsView
        fields = "__all__"



