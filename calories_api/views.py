from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from random import uniform as rnd
import pandas as pd
from .ImageFinder import get_images_links as find_image
from .model import recommend,output_recommended_recipes
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
import ast
from .models import *

# Create your views here.


dataset=pd.read_csv('datasets/meal_recommend/recipes.csv',compression='gzip')

nutritions_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']

meal_types=['Breakfast','Lunch','Dinner']

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
        day1 = [item[0] for item in recommendations]
        day2 = [item[1] for item in recommendations]
        day3 = [item[2] for item in recommendations]
        day4 = [item[3] for item in recommendations]
        day5 = [item[4] for item in recommendations]
        print(len(day1),len(day2),len(day3),len(day4),len(day5),"lengths")
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        for index,recipe in enumerate(day1):
            print(meal_types[index])
            recipeingrediants = ", ".join(recipe['RecipeIngredientParts'])
            recipeInstructions = ", ".join(recipe['RecipeInstructions'])
            try:
                rec = Recipe.objects.get(recipeid=recipe['RecipeId'])
                print(rec)
            except:
                recipeData = Recipe(RecipeId = recipe['RecipeId'], Name = recipe['Name'], RecipeIngredientParts = recipeingrediants, RecipeInstructions = recipeInstructions, Calories  = str(recipe['Calories']), FatContent = str(recipe['FatContent']), SaturatedFatContent = str(recipe['SaturatedFatContent']), CholesterolContent = str(recipe['CholesterolContent']), SodiumContent = str(recipe['SodiumContent']), CarbohydrateContent = str(recipe['CarbohydrateContent']), FiberContent = str(recipe['FiberContent']), SugarContent = str(recipe['SugarContent']), ProteinContent = str(recipe['ProteinContent']), CookTime = str(recipe['CookTime']), PrepTime = str(recipe['PrepTime']), TotalTime = str(recipe['TotalTime']), image_link = recipe['image_link'], meal_type = meal_types[index])
                recipeData.save()
                print(recipeData,"tars")
            data1.append(recipe['RecipeId'])
        print(data1)

        for index,recipe in enumerate(day2):
            recipeingrediants = ", ".join(recipe['RecipeIngredientParts'])
            recipeInstructions = ", ".join(recipe['RecipeInstructions'])
            try:
                rec = Recipe.objects.get(recipeid=recipe['RecipeId'])
                print(rec)
            except:
                recipeData = Recipe(RecipeId = recipe['RecipeId'], Name = recipe['Name'], RecipeIngredientParts = recipeingrediants, RecipeInstructions = recipeInstructions, Calories  = str(recipe['Calories']), FatContent = str(recipe['FatContent']), SaturatedFatContent = str(recipe['SaturatedFatContent']), CholesterolContent = str(recipe['CholesterolContent']), SodiumContent = str(recipe['SodiumContent']), CarbohydrateContent = str(recipe['CarbohydrateContent']), FiberContent = str(recipe['FiberContent']), SugarContent = str(recipe['SugarContent']), ProteinContent = str(recipe['ProteinContent']), CookTime = str(recipe['CookTime']), PrepTime = str(recipe['PrepTime']), TotalTime = str(recipe['TotalTime']), image_link = recipe['image_link'], meal_type = meal_types[index])
                recipeData.save()
                print(recipeData,"tars")
            data2.append(recipe['RecipeId'])
        print(data2)

        for index,recipe in enumerate(day3):
            recipeingrediants = ", ".join(recipe['RecipeIngredientParts'])
            recipeInstructions = ", ".join(recipe['RecipeInstructions'])
            try:
                rec = Recipe.objects.get(recipeid=recipe['RecipeId'])
                print(rec)
            except:
                recipeData = Recipe(RecipeId = recipe['RecipeId'], Name = recipe['Name'], RecipeIngredientParts = recipeingrediants, RecipeInstructions = recipeInstructions, Calories  = str(recipe['Calories']), FatContent = str(recipe['FatContent']), SaturatedFatContent = str(recipe['SaturatedFatContent']), CholesterolContent = str(recipe['CholesterolContent']), SodiumContent = str(recipe['SodiumContent']), CarbohydrateContent = str(recipe['CarbohydrateContent']), FiberContent = str(recipe['FiberContent']), SugarContent = str(recipe['SugarContent']), ProteinContent = str(recipe['ProteinContent']), CookTime = str(recipe['CookTime']), PrepTime = str(recipe['PrepTime']), TotalTime = str(recipe['TotalTime']), image_link = recipe['image_link'], meal_type = meal_types[index])
                recipeData.save()
                print(recipeData,"tars")
            data3.append(recipe['RecipeId'])
        print(data3)

        for index,recipe in enumerate(day4):
            recipeingrediants = ", ".join(recipe['RecipeIngredientParts'])
            recipeInstructions = ", ".join(recipe['RecipeInstructions'])
            try:
                rec = Recipe.objects.get(recipeid=recipe['RecipeId'])
                print(rec)
            except:
                recipeData = Recipe(RecipeId = recipe['RecipeId'], Name = recipe['Name'], RecipeIngredientParts = recipeingrediants, RecipeInstructions = recipeInstructions, Calories  = str(recipe['Calories']), FatContent = str(recipe['FatContent']), SaturatedFatContent = str(recipe['SaturatedFatContent']), CholesterolContent = str(recipe['CholesterolContent']), SodiumContent = str(recipe['SodiumContent']), CarbohydrateContent = str(recipe['CarbohydrateContent']), FiberContent = str(recipe['FiberContent']), SugarContent = str(recipe['SugarContent']), ProteinContent = str(recipe['ProteinContent']), CookTime = str(recipe['CookTime']), PrepTime = str(recipe['PrepTime']), TotalTime = str(recipe['TotalTime']), image_link = recipe['image_link'], meal_type = meal_types[index])
                recipeData.save()
                print(recipeData,"tars")
            data4.append(recipe['RecipeId'])
        print(data4)

        for index,recipe in enumerate(day5):
            recipeingrediants = ", ".join(recipe['RecipeIngredientParts'])
            recipeInstructions = ", ".join(recipe['RecipeInstructions'])
            try:
                rec = Recipe.objects.get(recipeid=recipe['RecipeId'])
                print(rec)
            except:
                recipeData = Recipe(RecipeId = recipe['RecipeId'], Name = recipe['Name'], RecipeIngredientParts = recipeingrediants, RecipeInstructions = recipeInstructions, Calories  = str(recipe['Calories']), FatContent = str(recipe['FatContent']), SaturatedFatContent = str(recipe['SaturatedFatContent']), CholesterolContent = str(recipe['CholesterolContent']), SodiumContent = str(recipe['SodiumContent']), CarbohydrateContent = str(recipe['CarbohydrateContent']), FiberContent = str(recipe['FiberContent']), SugarContent = str(recipe['SugarContent']), ProteinContent = str(recipe['ProteinContent']), CookTime = str(recipe['CookTime']), PrepTime = str(recipe['PrepTime']), TotalTime = str(recipe['TotalTime']), image_link = recipe['image_link'], meal_type = meal_types[index])
                recipeData.save()
                print(recipeData,"tars")
            data5.append(recipe['RecipeId'])
        print(data5)

        data = {'day1':data1, 'day2':data2, 'day3':data3, 'day4':data4, 'day5':data5}
        temp = reverse('generateDietPlan') + '?' + urlencode(data)
        url = "http:127.0.0.1:8000" + temp
        print(url)
        return Response({'url':url})
    except:
        return Response("Something went wrong. Please try again later.")

def generateDietPlan(request):
    day1 = request.GET.get('day1')
    day2 = request.GET.get('day2')
    day3 = request.GET.get('day3')
    day4 = request.GET.get('day4')
    day5 = request.GET.get('day5')
    day1 = ast.literal_eval(day1)
    day2 = ast.literal_eval(day2)
    day3 = ast.literal_eval(day3)
    day4 = ast.literal_eval(day4)
    day5 = ast.literal_eval(day5)

    day1_break = Recipe.objects.get(RecipeId = day1[0])
    day1_lunch = Recipe.objects.get(RecipeId = day1[1])
    day1_dinner = Recipe.objects.get(RecipeId = day1[2])

    day2_break = Recipe.objects.get(RecipeId = day2[0])
    day2_lunch = Recipe.objects.get(RecipeId = day2[1])
    day2_dinner = Recipe.objects.get(RecipeId = day2[2])

    day3_break = Recipe.objects.get(RecipeId = day3[0])
    day3_lunch = Recipe.objects.get(RecipeId = day3[1])
    day3_dinner = Recipe.objects.get(RecipeId = day3[2])

    day4_break = Recipe.objects.get(RecipeId = day4[0])
    day4_lunch = Recipe.objects.get(RecipeId = day4[1])
    day4_dinner = Recipe.objects.get(RecipeId = day4[2])

    day5_break = Recipe.objects.get(RecipeId = day5[0])
    day5_lunch = Recipe.objects.get(RecipeId = day5[1])
    day5_dinner = Recipe.objects.get(RecipeId = day5[2])

    day1_data = []
    day1_data.append(day1_break)
    day1_data.append(day1_lunch)
    day1_data.append(day1_dinner)

    day2_data = []
    day2_data.append(day2_break)
    day2_data.append(day2_lunch)
    day2_data.append(day2_dinner)

    day3_data = []
    day3_data.append(day3_break)
    day3_data.append(day3_lunch)
    day3_data.append(day3_dinner)

    day4_data = []
    day4_data.append(day4_break)
    day4_data.append(day4_lunch)
    day4_data.append(day4_dinner)

    day5_data = []
    day5_data.append(day5_break)
    day5_data.append(day5_lunch)
    day5_data.append(day5_dinner)
    
    return render(request, 'mealplannerhome.html', {'day1':day1_data, 'day2':day2_data, 'day3':day3_data, 'day4':day4_data, 'day5':day5_data})


def viewDietPlan(request, id):
    print(type(id))
    recipe = Recipe.objects.get(RecipeId=int(id))
    return render(request, 'mealdetail.html', {'recipe':recipe})


# http:127.0.0.1:8000/calories_api/genrate/?day1=%5B251706%2C+251706%2C+392241%5D&day2=%5B427097%2C+427097%2C+213776%5D&day3=%5B206870%2C+206870%2C+53234%5D&day4=%5B439996%2C+439996%2C+298290%5D&day5=%5B297358%2C+297358%2C+151135%5D