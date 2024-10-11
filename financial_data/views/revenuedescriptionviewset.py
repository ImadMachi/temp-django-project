from rest_framework import viewsets
from ..models import RevenuesView
from ..serializers import RevenueDescriptionSerializer


class RevenueDescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RevenueDescriptionSerializer

    def get_queryset(self):
        enterprise_id = self.request.query_params.get("enterprise_id")

        queryset = RevenuesView.objects.all()

        if enterprise_id:
            queryset = queryset.filter(enterprise=enterprise_id)

        # Get distinct combinations of description and revenue_id
        distinct_results = queryset.values("description", "revenue_id").distinct()

        # Create a list of dictionaries with enterprise, description, and revenue_id
        result = [
            {
                "enterprise": enterprise_id,
                "description": item["description"],
                "revenue_id": item["revenue_id"],
            }
            for item in distinct_results
        ]

        return result
