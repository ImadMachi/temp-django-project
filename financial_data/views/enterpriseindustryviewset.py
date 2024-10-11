from rest_framework import viewsets
from ..models import *
from ..serializers import *

class EnterpriseIndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnterpriseIndustryView.objects.all()
    serializer_class = EnterpriseIndustryViewSerializer



