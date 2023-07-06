from django.urls import path
from . import views
from healthcare_api.views import *

urlpatterns = [
    path('symptom/', SymptomApiEndPoint.as_view(), name='symptom'),
    path('qna/', QNAApiEndPoint.as_view(), name='qna'),
    path('disease/', DiseasePredictionApiEndPoint.as_view(), name='disease'),
]