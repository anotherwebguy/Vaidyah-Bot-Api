from django.shortcuts import render
import pymongo
import re
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
from . models import *
from . serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


#-------------------------------------------- mongodb connection --------------------------------------------

connection_string = "mongodb+srv://vaidyah:vaidyah123@cluster0.jbnvywb.mongodb.net/?retryWrites=true&w=majority"

client  = pymongo.MongoClient(connection_string)

#-------------------------------------------- diseas-symptoms ml model --------------------------------------------
data = pd.read_csv("datasets/disease_symptoms/disease-symptoms.csv")
cols= data.columns
cols= cols[:-1]
x = data[cols]
y = data['prognosis']

reduced_data = data.groupby(data['prognosis']).max()

#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

model  = DecisionTreeClassifier()
clf_model = model.fit(x_train,y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf_model, x_test, y_test, cv=3)
# print (scores)
print (scores.mean())

severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()

symptoms_dict = {}

for index, symptom in enumerate(x):
       symptoms_dict[symptom] = index

print(symptoms_dict)

def calc_condition(exp,days):
    sum=0
    for item in exp:
         sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        print("You should take the consultation from doctor. ")
    else:
        print("It might not be that bad but you should take precautions.")


def getDescription():
    global description_list
    with open('datasets/disease_symptoms/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)


def getSeverityDict():
    global severityDictionary
    with open('datasets/disease_symptoms/symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    global precautionDictionary
    with open('datasets/disease_symptoms/symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)

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
    
def sec_predict(symptoms_exp):
    df = pd.read_csv('datasets/disease_symptoms/disease-symptoms.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])


def print_disease(node):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))


getSeverityDict()
getDescription()
getprecautionDict()


# ---------------------------------------- Disease Prediction API EndPoints-------------------------------------------

class SymptomApiEndPoint(APIView):
    
        serializer_class = SymptomSerializer
        
        def post(self, request, format=None):
            serializer = SymptomSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data)
                input_data = serializer.data
                print(input_data["symptom"])
                print("hii")
                features=",".join(cols).split(",")
                input_data = input_data["symptom"].replace(" ","_")
                conf,cnf_dis=check_pattern(features,input_data)
                result = ""
                if conf==1:
                    result += "searches related to input: "+"\n"
                    for num,it in enumerate(cnf_dis):
                        result += str(num) + ")" + it + "\n"
                    if num!=0:
                        result += "Type the symptom you meant from the above to confirm:  " + "\n"
                    else:
                        result += "Confirm by typing the above symptom again:  " + "\n"
                else:
                    result += "Enter valid symptom."
                return Response(result)
            

class QNAApiEndPoint(APIView):
    
        serializer_class = ConfirmSymptomSerializer
        
        def post(self, request, format=None):
            serializer = ConfirmSymptomSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data)
                input_data = serializer.data
                print(input_data["confirm_symptom"])
                input_data = input_data["confirm_symptom"].replace(" ","_")
                tree_ = clf_model.tree_
                feature_name = [
                    cols[i] if i != _tree.TREE_UNDEFINED else "undefined!"
                    for i in tree_.feature
                ]
                symptoms_present = []
                def recurse(node, depth):
                    indent = "  " * depth
                    print(indent,"indent")
                    if tree_.feature[node] != _tree.TREE_UNDEFINED:
                        print(tree_.feature[node],"dekho")
                        name = feature_name[node]
                        threshold = tree_.threshold[node]
                        if name == input_data:
                            val = 1
                        else:
                            val = 0
                        if  val <= threshold:
                            return recurse(tree_.children_left[node], depth + 1)
                        else:
                            symptoms_present.append(name)
                            return recurse(tree_.children_right[node], depth + 1)
                    else:
                        pres_disease = print_disease(tree_.value[node])
                        red_cols = reduced_data.columns 
                        symptoms_given = red_cols[reduced_data.loc[pres_disease].values[0].nonzero()]
                        result = "Are you experiencing any " + "\n"
                        for syms in list(symptoms_given):
                            print(syms, "ksjj")
                            result += syms+"? : \n"
                            
                        result += "Please type all that applies in the format : eg. cold, fatigue, headache " + "\n"
                        return result,pres_disease
                result,pres = recurse(0, 1)
                print(pres[0],"pres")
                disease = PresentDisease(disease=str(pres[0]))
                disease.save()
                return Response(result)
            

class DiseasePredictionApiEndPoint(APIView):
    
        serializer_class = QNASerializer
        
        def post(self, request, format=None):
            serializer = QNASerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data)
                input_data = serializer.data
                print(input_data["answers"])
                print("hii")
                present_disease = PresentDisease.objects.all().order_by('-id')[:1]
                print(present_disease[0].disease,"present_disease")
                symptoms_exp = input_data["answers"].split(", ")
                symptoms_exp = [item.replace(" ", "_") for item in symptoms_exp]
                print(symptoms_exp)
                result = ""
                second_prediction=sec_predict(symptoms_exp)
                if(present_disease[0].disease==second_prediction[0]):
                    result += "You may have " + present_disease[0].disease + "\n"
                    result += description_list[present_disease[0].disease] + "\n"
                else:
                    result += "You may have " + present_disease[0].disease + "or " + second_prediction[0] + "\n"
                    result += description_list[present_disease[0].disease] + "\n"
                    result += description_list[second_prediction[0]] + "\n"

                precution_list1=precautionDictionary[present_disease[0].disease]
                precution_list2=precautionDictionary[second_prediction[0]]
                result += "Take following measures for" + present_disease[0].disease +" : " + "\n"
                for  i,j in enumerate(precution_list1):
                    result += str(i+1) + ")" +j + "\n"
                
                if(present_disease[0].disease!=second_prediction[0]):
                    result += "Take following measures for" + second_prediction[0] +" : " + "\n"
                    for  i,j in enumerate(precution_list2):
                        result += str(i+1) + ")" +j + "\n"

                return Response(result)

