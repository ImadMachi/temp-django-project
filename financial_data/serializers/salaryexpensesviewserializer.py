from rest_framework import serializers
from ..models import *

class SalaryExpensesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryExpensesView
        fields = "__all__"



