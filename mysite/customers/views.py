from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from mongo_auth.permissions import AuthenticatedOnly

from .models import Customer
from .serializers import CustomerSerializer
import json
from rest_framework.decorators import api_view
from mongo_auth.utils import create_unique_object_id, pwd_context
from mongo_auth.db import database, auth_collection, fields, jwt_life, jwt_secret, secondary_username_field
import jwt
import datetime
from mongo_auth import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from bson import ObjectId
from bson.json_util import dumps

class CustomerView(APIView):

    #permission_classes = [AuthenticatedOnly]
    def get(self, request):
        serializer = CustomerSerializer(Customer.objects.all(), many=True)
        response = {"customers": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    
    def post(self, request, format=None):

        data = request.data
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():

            customer = Customer(**data)
            json_valid = serializer.data
            data = validate_customer_exists(json_valid["customerId"])
            #return Response(data, status=status.HTTP_200_OK)
            if not data:
                customer.save()
                response = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "Ya existe el cliente"})
    
def validate_customer_exists(data):
    data = database["customer"].find_one({"customerId": data})
    data = json.loads(dumps(data))
    return data