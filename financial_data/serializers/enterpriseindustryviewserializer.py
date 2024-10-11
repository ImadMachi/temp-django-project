from rest_framework import serializers
from ..models import *

class EnterpriseIndustryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterpriseIndustryView
        fields = "__all__"



