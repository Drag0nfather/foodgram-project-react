from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe.views import TagViewSet, RecipeViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
