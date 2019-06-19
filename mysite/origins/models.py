from django.db import models

from mongoengine import *
from bson.objectid import ObjectId

class Origin(Document):
    _id = ObjectIdField(required=True, default=ObjectId, primary_key=True)
    originId = StringField(required=True)
    description = StringField(required=True)
