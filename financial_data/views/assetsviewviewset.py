from rest_framework import viewsets
from ..models import *
from ..serializers import *

class AssetsViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssetsView.objects.all()
    serializer_class = AssetsViewSerializer



