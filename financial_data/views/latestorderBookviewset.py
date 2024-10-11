from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Max
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import get_object_or_404
from financial_data.models.orderbook import OrderBook
from financial_data.models.enterprise import Enterprise

from financial_data.serializers.orderbookserializer import OrderBookSerializer


class LatestOrderBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderBook.objects.all()
    serializer_class = OrderBookSerializer

    def retrieve(self, request, pk=None):
        enterprise = get_object_or_404(Enterprise, pk=pk)
        latest_orderbook = (
            OrderBook.objects.filter(enterprise=enterprise)
            .order_by("-created_at", "-active")
            .first()
        )

        if latest_orderbook:
            # Round the total to two decimal places
            rounded_total = Decimal(latest_orderbook.total).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            response_data = {
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.name,
                "latest_total": str(rounded_total),
                "created_at": latest_orderbook.created_at,
                "year": latest_orderbook.year,
                "active": latest_orderbook.active,
            }
            return Response(response_data)
        else:
            return Response(
                {"detail": "No order book found for this enterprise."}, status=404
            )
