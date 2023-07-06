from . models import *
from rest_framework import serializers

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

class ConfirmSymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmSymptom
        fields = '__all__'

class QNASerializer(serializers.ModelSerializer):
    class Meta:
        model = QNA
        fields = '__all__'