from rest_framework import serializers
from ..models import *

class RevenuesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenuesView
        fields = "__all__"



