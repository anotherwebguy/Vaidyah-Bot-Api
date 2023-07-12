from django.urls import path
from . import views
from info_api.views import *

urlpatterns = [
    path('disease/', views.getDisease, name='disease'),
    path('symptoms/', views.getSymptoms, name='symptoms'),
    path('info/', views.getInfo, name='info'),
    path('prevent/', views.getPrevention, name='prevent'),
    path('cause/', views.getCause, name='cause'),
    path('desc/', views.getDescription, name='desc'),
]