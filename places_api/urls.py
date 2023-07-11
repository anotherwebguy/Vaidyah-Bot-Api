from django.urls import path
from . import views
from places_api.views import *

urlpatterns = [
    path('nearby/', views.getNearbyHospitals, name='nearby'),
]