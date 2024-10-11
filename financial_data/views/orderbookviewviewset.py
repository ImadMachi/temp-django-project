from rest_framework import viewsets
from ..models import *
from ..serializers import *


class OrderBookViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderBookView.objects.all()
    serializer_class = OrderBookViewSerializer
