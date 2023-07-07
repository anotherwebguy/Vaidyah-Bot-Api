from django.urls import path
from . import views
from healthcare_api.views import *

urlpatterns = [
    path('symptom/', views.getSymptoms, name='symptom'),
    # path('qna/', views.getQNA, name='qna'),
    path('disease/', views.getDiagnosis, name='disease'),
]