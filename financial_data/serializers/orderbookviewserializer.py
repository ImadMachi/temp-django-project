from rest_framework import serializers
from ..models import *

class OrderBookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBookView
        fields = "__all__"



