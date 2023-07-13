from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from random import uniform as rnd
import pandas as pd
from .ImageFinder import get_images_links as find_image
from .model import recommend,output_recommended_recipes

# Create your views here.


dataset=pd.read_csv('datasets/meal_recommend/recipes.csv',compression='gzip')

nutritions_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']

meals_calories_perc={'breakfast':0.35,'lunch':0.40,'dinner':0.25}

def Generator(recommended_nutrition):
    recommendation_dataframe=recommend(dataset,recommended_nutrition)
    output=output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output":None}
    else:
        return {"output":output}

def generate_recommendations(calories,weight_loss):
    total_calories=weight_loss*calories
    recommendations=[]
    print(total_calories)
    for meal in meals_calories_perc:
        meal_calories=meals_calories_perc[meal]*total_calories
        print(meal_calories)
        if meal=='breakfast':        
            recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
        elif meal=='launch':
            recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
        elif meal=='dinner':
            recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
        generator=Generator(recommended_nutrition)
        print("Generating...")
        recommended_recipes=generator['output']
        recommendations.append(recommended_recipes)
    for recommendation in recommendations:
        for recipe in recommendation:
            recipe.pop('RecipeId')
            recipe.pop('RecipeIngredientParts')
            recipe['image_link']=find_image(recipe['Name']) 
    return recommendations

@api_view(['GET'])
def getDailyCalories(request):
    try:
        val = request.GET.get('val')
        print(val)
        data = val.split(' , ')
        print(data)
        # calories = 0.0
        if data[0] == 'Male':
            calories = 10 * int(data[3]) + 6.25 * int(data[2]) - 5 * int(data[1]) + 5
        else:   
            calories = 10 * int(data[3]) + 6.25 * int(data[2]) - 5 * int(data[1]) - 161
        print(calories)
        if data[4] == 'Sedentary':
            calories *= 1.2
        elif data[4] == 'Lightly Active':
            calories *= 1.375
        elif data[4] == 'Moderately Active':
            calories *= 1.55
        elif data[4] == 'Very Active':
            calories *= 1.725
        else:
            calories *= 1.9
        print(calories)
        calories = round(calories)
        print(calories)
        loss = calories - 500
        gain = calories + 500
        val = int(data[2])/100
        bmi = int(data[3]) / (val * val)
        category = ''
        if bmi<18.5:
            category='Underweight'
        elif 18.5<=bmi<25:
            category='Normal'
        elif 25<=bmi<30:
            category='Overweight'
        else:
            category='Obesity'   
        return Response({'calories':calories,'loss':loss,'gain':gain,'bmi':bmi,'category':category})
    except:
        return Response("Something went wrong. Please try again later.")
    
@api_view(['GET'])
def getRecommendedRecipes(request):
    try:
        val = request.GET.get('val')
        calories,weight_loss = val.split(' , ')
        weight_loss = float(weight_loss)
        calories = int(calories)
        print(calories,weight_loss)
        recommendations = generate_recommendations(calories,weight_loss)
        breakfast = recommendations[0]
        lunch = recommendations[1]
        dinner = recommendations[2]
        return Response({'breakfast':breakfast,'lunch':lunch,'dinner':dinner})
    except:
        return Response("Something went wrong. Please try again later.")
