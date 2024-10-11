from rest_framework import viewsets
from ..models import *
from ..serializers import *

class OpportunityBookViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OpportunityBookView.objects.all()
    serializer_class = OpportunityBookViewSerializer



