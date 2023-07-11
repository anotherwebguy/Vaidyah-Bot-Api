from django.urls import path
from . import views
from nutrition_api.views import *

urlpatterns = [
    path('food/', views.getFoodNutrients, name='food'),
    path('exercise/', views.getExercise, name='excercise'),
]