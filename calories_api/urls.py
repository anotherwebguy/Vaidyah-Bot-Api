from django.urls import path
from . import views
from calories_api.views import *

urlpatterns = [
    path('calories/', views.getDailyCalories, name='calories'),
    path('recipe/', views.getRecommendedRecipes, name='recipe'),
]