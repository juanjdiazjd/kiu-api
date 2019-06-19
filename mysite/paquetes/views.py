from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from mongo_auth.permissions import AuthenticatedOnly

from .models import Paquete
from .serializers import PaqueteSerializer
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

class PaqueteView(APIView):

    #permission_classes = [AuthenticatedOnly]
    def get(self, request):
	    serializer = PaqueteSerializer(Paquete.objects.all(), many=True)
	    response = {"paquetes": serializer.data}
	    return Response(response, status=status.HTTP_200_OK)



    def post(self, request, format=None):

        data = request.data
        data["price"] = 10
        serializer = PaqueteSerializer(data=data)
        if serializer.is_valid():

            paquete = Paquete(**data)
            json_valid = serializer.data
            origin = json_valid["originId"]
            destiny = json_valid["destinyId"]
            customerId = json_valid["customerId"]
            paqueteId = json_valid["paqueteId"]
            if origin != destiny:    
                success_origin_destiny, origin, destiny = validate_origin_destiny(origin,destiny)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "Origen y destino no pueden ser iguales"})
            if not success_origin_destiny:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "Origen o destino no existe"})
            success_customer, customer = validate_customer(customerId)
            if not success_customer:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": customer})
            success_paquete,data = validate_paquete(paqueteId)
            if not success_paquete:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "paqueteId ya existe"})
            #return Response(serializer.data, status=status.HTTP_200_OK)
            paquete.save()
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)


def validate_customer(customerId):
        if json.loads(dumps(database["customer"].find_one({"customerId": customerId}))):
            return True, customerId

        return False, "No existe cliente"
def validate_origin_destiny(origin,destiny):
        if json.loads(dumps(database["origin"].find_one({"originId": origin}))) and json.loads(dumps(database["origin"].find_one({"originId": destiny}))):
            return True, origin, destiny
        return False, origin, destiny

def validate_paquete(paqueteId):
    data = database["paquete"].find_one({"paqueteId": paqueteId})
    data = json.loads(dumps(data))
    if data:
        return False, data
    return True, data

@api_view(["POST"])
def obtenerTotalPorFecha(request):
    try:
        data = request.data
        if not 'fecha' in data:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "fecha no puede ser nulo"})

        db_response = json.loads(dumps(database["paquete"].find({"createdAt": data["fecha"]})))
        final_count = sumPrice(db_response)
        if not db_response:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"error_msg": "No hay registros para este día"})
        response = {"Total de paquetes transportados: ":len(db_response),"Total recaudado en la siguiente fecha "+ data["fecha"] +": ":final_count}    
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"data": {"error_msg": str(e)}})

def sumPrice(list):
    count=0
    for x in list:
        count +=x["price"]
    return count
