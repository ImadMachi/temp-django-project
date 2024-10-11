from rest_framework import serializers
from ..models import *

class AssetsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsView
        fields = "__all__"



