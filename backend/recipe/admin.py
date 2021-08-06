from django.contrib import admin
from django.shortcuts import get_object_or_404

from .models import Tag, Recipe, Ingredient, IngredientInRecipe


class RecipeIngredientInLine(admin.TabularInline):
    model = IngredientInRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_favorited')
    search_fields = ('user', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = [RecipeIngredientInLine]

    def is_favorited(self, request):
        recipe = get_object_or_404(Recipe, id=request.id)
        return recipe.is_favorited.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(IngredientInRecipe)
