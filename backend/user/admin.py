from django.contrib import admin

from user.models import Follow, ShoppingCart, FavouriteRecipe


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Follow)
admin.site.register(ShoppingCart)
admin.site.register(FavouriteRecipe)
