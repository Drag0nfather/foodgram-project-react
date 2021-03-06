from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    name = models.CharField(max_length=50, blank=False, unique=True,)
    color = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    name = models.CharField(max_length=60, blank=False, unique=True)
    measurement_unit = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False)
    name = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to='static/', blank=False, null=False)
    text = models.TextField(max_length=1000, blank=False)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientInRecipe', related_name='recipes', blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    cooking_time = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='amounts')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='amounts')
    amount = models.IntegerField(blank=False, null=False)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='recipe_ingredient_unique')]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'Количество "{self.ingredient}" в рецепте "{self.recipe}"'
