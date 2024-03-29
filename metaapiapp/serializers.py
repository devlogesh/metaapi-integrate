from rest_framework import serializers
from .models import *

class PagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = pagePost
        fields = '__all__'