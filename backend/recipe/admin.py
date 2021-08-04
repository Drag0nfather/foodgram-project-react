from django.contrib import admin

from .models import Tag, Recipe, Ingredient, IngredientInRecipe


class RecipeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientInRecipe)