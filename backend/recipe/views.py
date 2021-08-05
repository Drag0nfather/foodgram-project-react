from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from recipe.filters import RecipeFilter
from recipe.models import Tag, Recipe, Ingredient
from recipe.permissions import AuthPostRetrieve, IsAuthorOrReadOnly
from recipe.serializers import TagSerializer, IngredientReadSerializer, RecipeReadSerializer, RecipeWriteSerializer, \
    FavouriteSerializer, ShoppingCartSerializer
from user.models import FavouriteRecipe, ShoppingCart


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
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            if not user.is_favorited.filter(recipe=recipe).exists():
                FavouriteRecipe.objects.create(user=user, recipe=recipe)
                serializer = FavouriteSerializer(recipe,
                                                 context={'request': request})
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {'errors': 'Этот рецепт уже есть в избранном'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_favorited.filter(recipe=recipe).exists():
            data = {'errors': 'Этого рецепта не было в вашем избранном'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        FavouriteRecipe.objects.filter(user=user, recipe=recipe).delete()
        data = {'deleted': 'success'}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            if not user.is_in_shopping_cart.filter(recipe=recipe).exists():
                ShoppingCart.objects.create(user=user, recipe=recipe)
                serializer = ShoppingCartSerializer(
                    recipe, context={'request': request})
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {'errors': 'Этот рецепт уже есть в списке покупок'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_in_shopping_cart.filter(recipe=recipe).exists():
            data = {'errors': 'Этого рецепта не было в вашем списке покупок'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        data = {'deleted': 'success'}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
