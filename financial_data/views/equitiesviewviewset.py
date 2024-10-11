from rest_framework import viewsets
from ..models import *
from ..serializers import *

class EquitiesViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EquitiesView.objects.all()
    serializer_class = EquitiesViewSerializer



