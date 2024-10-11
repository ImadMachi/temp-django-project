from rest_framework import serializers
from ..models import *

class IndustryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryType
        fields = "__all__"



