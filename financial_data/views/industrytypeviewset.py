from rest_framework import viewsets
from ..models import *
from ..serializers import *

class IndustryTypeViewSet(viewsets.ModelViewSet):
    queryset = IndustryType.objects.all()
    serializer_class = IndustryTypeSerializer



