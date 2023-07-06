from django.db import models

# Create your models here.
class Symptom(models.Model):
    symptom = models.CharField(max_length=100)

class ConfirmSymptom(models.Model):
    confirm_symptom = models.CharField(max_length=100)

class QNA(models.Model):
    answers = models.CharField(max_length=1000)

class PresentDisease(models.Model):
    disease = models.CharField(max_length=100)
