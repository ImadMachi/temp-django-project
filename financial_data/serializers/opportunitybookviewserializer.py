from rest_framework import serializers
from ..models import *

class OpportunityBookViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpportunityBookView
        fields = "__all__"



