import pymongo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import dotenv_values
import pandas as pd
import re

env_vars = dotenv_values(".env")

MONGO_USERNAME = env_vars['MONGO_USERNAME']
MONGO_PASSWORD = env_vars['MONGO_PASSWORD']

connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.jbnvywb.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)
db = client['Medical_Analysis']
collection = db.analysis

data = pd.read_csv("datasets/disease_symptoms/medical_kb.csv")
diseases = data['name'].unique()

# print(diseases)

def check_pattern(dis_list,inp):
    pred_list=[]
    inp=inp.replace(' ','_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list=[item for item in dis_list if regexp.search(item)]
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return 0,[]

# Create your views here.

@api_view()
def getDisease(request):
    try:
        disease = request.GET.get('disease')
        input_data = disease
        conf,cnf_dis=check_pattern(diseases,input_data)
        result = []
        if conf==1:
            for num,it in enumerate(cnf_dis):
                result.append(it)
        return Response({'data':result})
    except:
        return Response({'data':"Enter Valid Symptom"})
    

@api_view()
def getSymptoms(request):
    try:
        disease = request.GET.get('disease')
        input_data = disease
        query = {"name": input_data}
        document = collection.find_one(query)
        result = []
        if document:
            result = document['symptom']
        return Response({'data':result})
    except:
        return Response({'data':"Enter Valid Disease"})
    
@api_view()
def getInfo(request):
    try:
        disease = request.GET.get('disease')
        input_data = disease
        query = {"name": input_data}
        document = collection.find_one(query)
        name = document['name']
        desc = document['desc']
        symptoms = document['symptom']
        prevent = document['prevent']
        cause = document['cause']
        cure_dept = document['cure_department']
        cure_way = document['cure_way']
        return Response({'name':name,'desc':desc,'symptoms':symptoms,'prevent':prevent,'cause':cause,'cure_dept':cure_dept,'cure_way':cure_way})
    except:
        return Response({'data':"Enter Valid Disease"})
    
@api_view()
def getPrevention(request):
    try:
        disease = request.GET.get('disease')
        input_data = disease
        query = {"name": input_data}
        document = collection.find_one(query)
        result = document['prevent']
        return Response({'data':result})
    except:
        return Response({'data':"Enter Valid Disease"})
    
@api_view()
def getCause(request):
    try:
        disease = request.GET.get('disease')
        input_data = disease
        query = {"name": input_data}
        document = collection.find_one(query)
        result = document['cause']
        return Response({'data':result})
    except:
        return Response({'data':"Enter Valid Disease"})
    
@api_view()
def getDescription(request):
    try:
        disease = request.GET.get('disease')
        input_data = disease
        query = {"name": input_data}
        document = collection.find_one(query)
        result = document['desc']
        return Response({'data':result})
    except:
        return Response({'data':"Enter Valid Disease"})


    
    


