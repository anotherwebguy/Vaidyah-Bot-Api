import pymongo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

MONGO_USERNAME = env_vars['MONGO_USERNAME']
MONGO_PASSWORD = env_vars['MONGO_PASSWORD']

connection_string = "mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.jbnvywb.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)

# Create your views here.

