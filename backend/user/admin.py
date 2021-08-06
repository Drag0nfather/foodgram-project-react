from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import Follow, ShoppingCart, FavouriteRecipe, User


class UserAdmin(UserAdmin):
    list_filter = ("first_name", "email")


admin.site.register(Follow)
admin.site.register(ShoppingCart)
admin.site.register(FavouriteRecipe)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
