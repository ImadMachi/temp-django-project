from rest_framework import serializers
from ..models import *

class ExpensesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesView
        fields = "__all__"



