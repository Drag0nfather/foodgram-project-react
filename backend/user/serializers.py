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

    @staticmethod
    def get_is_subscribed(obj):
        if not obj.is_authenticated:
            return False
        return obj.following.filter(user__in=User.objects.all()).exists()


class UserOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(max_length=150, required=True, allow_blank=False)
    last_name = serializers.CharField(max_length=150, required=True, allow_blank=False)
    email = serializers.EmailField()




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
