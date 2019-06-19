
from rest_framework_mongoengine import serializers

from .models import Origin

class OriginSerializer(serializers.DocumentSerializer):
    class Meta:
    	model = Origin
    	fields = '__all__'