import pymongo
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')

connection_string = "mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.jbnvywb.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)

# Create your views here.

