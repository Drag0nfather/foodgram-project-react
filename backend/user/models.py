from django.contrib.auth import get_user_model
from django.db import models
from recipe.models import Recipe

User = get_user_model()


class Follow(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique follow')]
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='user_favourite')]


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='user_purchases')]
