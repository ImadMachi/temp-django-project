from rest_framework import serializers
from ..models import *

class EquitiesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquitiesView
        fields = "__all__"



