from rest_framework import serializers

from recipe.models import Recipe
from .models import User


class SubRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return obj.following.filter(user=user).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.following.filter(user=user).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = int(request.query_params.get('recipes_limit', 3))
        recipes = Recipe.objects.filter(author=obj)
        serializer = SubRecipeSerializer(recipes, many=True,
                                         context={'request': request})
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    model = User
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
