from rest_framework import serializers
from ..models import *

class LiabilitiesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiabilitiesView
        fields = "__all__"



