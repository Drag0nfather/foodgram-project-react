from django.contrib import admin

from .models import Tag, Ingredient, Recipe


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
