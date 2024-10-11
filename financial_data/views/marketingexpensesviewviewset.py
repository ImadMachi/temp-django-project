from rest_framework import viewsets
from ..models import *
from ..serializers import *

class MarketingExpensesViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MarketingExpensesView.objects.all()
    serializer_class = MarketingExpensesViewSerializer



