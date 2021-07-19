from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               null=False)
    name = models.CharField(max_length=50, blank=False)
    image = models.ImageField(upload_to='static/', blank=False, null=False)
    text = models.TextField(max_length=1000, blank=False)
    ingredient = models.ManyToManyField(Ingredient, blank=False, null=False)
    tag = models.ManyToManyField(Tag, blank=False, null=False)
    cooking_time = models.IntegerField(blank=False, null=False)
