from django.urls import path
from . import views
from healthcare_api.views import *

urlpatterns = [
    path('disease/', views.index, name='index'),
]