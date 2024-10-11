from rest_framework import viewsets
from ..models import *
from ..serializers import *

class SalaryExpensesViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalaryExpensesView.objects.all()
    serializer_class = SalaryExpensesViewSerializer



