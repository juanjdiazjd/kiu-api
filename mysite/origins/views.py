from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from mongo_auth.permissions import AuthenticatedOnly

from .models import Origin
from .serializers import OriginSerializer
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

class OriginView(APIView):

    #permission_classes = [AuthenticatedOnly]

    def get(self, request):
        serializer = OriginSerializer(Origin.objects.all(), many=True)
        response = {"origins": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    
    def post(self, request, format=None):

    	data = request.data
    	serializer = OriginSerializer(data=data)
    	if serializer.is_valid():

            origin = Origin(**data)
            json_valid = serializer.data
            data = validate_origin_destiny_exists(json_valid["originId"])
            #return Response(data, status=status.HTTP_200_OK)
            if not data:
                origin.save()
                response = serializer.data
                return Response(response, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "Ya existe el origen o destino"})
    
def validate_origin_destiny_exists(data):
    data = database["origin"].find_one({"originId": data})
    data = json.loads(dumps(data))
    return data