from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal, ROUND_HALF_UP
from financial_data.models.enterprise import Enterprise
from financial_data.models.opportunitybook import OpportunityBook
from financial_data.serializers.opportunitybookSerializer import (
    OpportunityBookSerializer,
)


class LatestOpportunityBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OpportunityBook.objects.all()
    serializer_class = OpportunityBookSerializer

    def retrieve(self, request, pk=None):
        enterprise = get_object_or_404(Enterprise, pk=pk)
        latest_opportunitybook = (
            OpportunityBook.objects.filter(enterprise=enterprise)
            .order_by("-created_at", "-active")
            .first()
        )

        if latest_opportunitybook:
            # Round the total to two decimal places
            rounded_total = Decimal(latest_opportunitybook.total).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            response_data = {
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.name,
                "latest_total": str(rounded_total),
                "created_at": latest_opportunitybook.created_at,
                "year": latest_opportunitybook.year,
                "active": latest_opportunitybook.active,
            }
            return Response(response_data)
        else:
            return Response(
                {"detail": "No opportunity book found for this enterprise."}, status=404
            )
