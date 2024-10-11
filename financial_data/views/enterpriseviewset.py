from rest_framework import viewsets
from ..models import *
from ..serializers import *

class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer



