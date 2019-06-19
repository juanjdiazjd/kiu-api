
from rest_framework_mongoengine import serializers

from .models import Customer

class CustomerSerializer(serializers.DocumentSerializer):
    class Meta:
    	model = Customer
    	fields = '__all__'