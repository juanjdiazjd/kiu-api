
from rest_framework_mongoengine import serializers

from .models import Paquete

class PaqueteSerializer(serializers.DocumentSerializer):
    class Meta:
    	model = Paquete
    	fields = '__all__'