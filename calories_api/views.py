from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

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
        return Response({'calories':calories,'loss':loss,'gain':gain})
    except:
        return Response("Something went wrong. Please try again later.")
