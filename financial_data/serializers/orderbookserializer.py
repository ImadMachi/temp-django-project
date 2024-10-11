from rest_framework import serializers
from financial_data.models.orderbook import OrderBook
from .enterpriseserializer import (
    EnterpriseSerializer,
)  # Import your existing Enterprise serializer


class OrderBookSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseSerializer(read_only=True)

    class Meta:
        model = OrderBook
        fields = ["id", "enterprise", "name", "created_at", "year", "total", "active"]
