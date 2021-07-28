from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from recipe.models import Tag, Recipe, Ingredient
from recipe.permissions import AuthPostRetrieve, IsAuthorOrReadOnly
from recipe.serializers import TagSerializer, IngredientReadSerializer, RecipeReadSerializer, RecipeWriteSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RecipeViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [AuthPostRetrieve, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
