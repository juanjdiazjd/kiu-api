from django.db import models

from mongoengine import *
from bson.objectid import ObjectId
import datetime
datetime_now= datetime.datetime.now().strftime('%Y-%m-%d')

class Paquete(Document):
    _id = ObjectIdField(required=True, default=ObjectId, primary_key=True)
    paqueteId = StringField(required=True)
    customerId = StringField(required=True)
    originId = StringField(required=True)
    destinyId = StringField(required=True)
    price = FloatField(required=True)
    createdAt = StringField(default=datetime_now)
