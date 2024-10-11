from rest_framework import serializers
from ..models import *

class MarketingExpensesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingExpensesView
        fields = "__all__"



