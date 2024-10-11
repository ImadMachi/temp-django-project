from rest_framework import viewsets
from ..models import *
from ..serializers import *

class SalesBudgetsViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalesBudgetsView.objects.all()
    serializer_class = SalesBudgetsViewSerializer



