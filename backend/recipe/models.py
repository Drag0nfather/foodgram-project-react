from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True,)
    color = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    measurement_unit = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False)
    name = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to='static/', blank=False, null=False)
    text = models.TextField(max_length=1000, blank=False)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInRecipe', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    cooking_time = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.ingredient
