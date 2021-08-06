from django.contrib.auth import get_user_model
from django.db import models
from recipe.models import Recipe

User = get_user_model()


class Follow(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique follow')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')

    def __str__(self):
        return f'Пользователь "{self.user}" подписан на пользователя "{self.author}"'


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='is_favorited')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='is_favorited')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='user_favourite')]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe.name} в избранном у пользователя ' \
               f'{self.user.username}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='is_in_shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='is_in_shopping_cart')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='user_purchases')]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'"{self.recipe}" в списке покупок у "{self.user}"'
