from django.db import models

# Create your models here.

class Recipe(models.Model):
    RecipeId = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    RecipeIngredientParts = models.CharField(max_length=10000)
    RecipeInstructions = models.CharField(max_length=10000)
    Calories = models.CharField(max_length=100)
    FatContent = models.CharField(max_length=100)
    SaturatedFatContent = models.CharField(max_length=100)
    CholesterolContent = models.CharField(max_length=100)
    SodiumContent = models.CharField(max_length=100)
    CarbohydrateContent = models.CharField(max_length=100)
    FiberContent = models.CharField(max_length=100)
    SugarContent = models.CharField(max_length=100)
    ProteinContent = models.CharField(max_length=100)
    CookTime = models.CharField(max_length=100)
    PrepTime = models.CharField(max_length=100)
    TotalTime = models.CharField(max_length=100)
    image_link = models.CharField(max_length=10000)
    meal_type = models.CharField(max_length=100,default="Breakfast")
    def __str__(self):
        return self.Name
