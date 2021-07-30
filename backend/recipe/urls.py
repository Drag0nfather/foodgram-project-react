from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagViewSet, RecipeViewSet, IngredientViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
