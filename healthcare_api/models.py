from django.db import models

# Create your models here.

class PresentDisease(models.Model):
    disease = models.CharField(max_length=100)
