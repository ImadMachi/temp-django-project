from rest_framework import viewsets
from ..models import *
from ..serializers import *

class ExpensesViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExpensesView.objects.all()
    serializer_class = ExpensesViewSerializer



