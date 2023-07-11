from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import dotenv_values
import requests

env_vars = dotenv_values(".env")
app_id = env_vars['NUTRITIONIX_APP_ID']
app_key = env_vars['NUTRITIONIX_APP_KEY']

# Create your views here.

@api_view(['GET'])
def getFoodNutrients(request):
    try:
        food = request.GET.get('food')
        print(food)

        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "Content-Type": "application/json",
            "x-app-id": app_id,
            "x-app-key": app_key,
        }

        data = {
            "query": food,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            # Request successful
            res = response.json()
            # Process the result as needed
            print(res)
            result = [
                [
                    food['food_name'],
                    food['serving_unit'],
                    str(food['serving_qty']),
                    str(food['nf_calories']),
                    str(food['nf_total_fat']),
                    str(food['nf_cholesterol']),
                    str(food['nf_protein']),
                ]
                for food in res['foods']
            ]
            return Response(result)
        else:
            # Request failed
            print("Error:", response.status_code)
            return Response("Can't recognize food item. Please try again.")
    except:
        return Response("Something went wrong. Please try again later.")


@api_view(['GET'])
def getExercise(request):
    try:
        exercise = request.GET.get('exercise')
        print(exercise)

        url = "https://trackapi.nutritionix.com/v2/natural/exercise"
        headers = {
            "Content-Type": "application/json",
            "x-app-id": app_id,
            "x-app-key": app_key,
        }

        data = {
            "query": exercise,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            # Request successful
            res = response.json()
            # Process the result as needed
            print(res)
            result = [
                [
                    exer['name'],
                    str(exer['duration_min']),
                    str(exer['met']),
                    str(exer['nf_calories']),
                ]
                for exer in res['exercises']
            ]
            return Response(result)
        else:
            # Request failed
            print("Error:", response.status_code)
            return Response("Can't recognize the excercise. Please try again.")
    except:
        return Response("Something went wrong. Please try again later.")



