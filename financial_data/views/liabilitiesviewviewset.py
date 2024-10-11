from rest_framework import viewsets
from ..models import *
from ..serializers import *

class LiabilitiesViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LiabilitiesView.objects.all()
    serializer_class = LiabilitiesViewSerializer



