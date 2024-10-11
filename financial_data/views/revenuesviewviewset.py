from rest_framework import viewsets
from ..models import *
from ..serializers import *

class RevenuesViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RevenuesView.objects.all()
    serializer_class = RevenuesViewSerializer



