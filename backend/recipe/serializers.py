import base64
import imghdr
import uuid

import six
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Tag, Recipe, Ingredient, IngredientInRecipe, User


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = '%s.%s' % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        if extension == 'jpeg':
            extension = 'jpg'
        return extension  # noqa R504


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        model = User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'colour', 'slug')
        model = Tag


class IngredientReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientInRecipeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')
        model = Recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(read_only=True, many=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time')


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        ingredients_set = set()
        for ingredient in ingredients_data:
            if ingredient['amount'] < 0:
                raise serializers.ValidationError(
                    'Количество должно быть >= 0')
            if ingredient['id'] in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.')
            ingredients_set.add(ingredient['id'])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            IngredientInRecipe.objects.create(
                ingredient=get_object_or_404(IngredientInRecipe, id=id),
                recipe=recipe, amount=amount
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients_set = set()
        for ingredient in ingredients_data:
            if ingredient['amount'] < 0:
                raise serializers.ValidationError(
                    'Количество должно быть >= 0')
            if ingredient['id'] in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.')
            ingredients_set.add(ingredient['id'])
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            IngredientInRecipe.objects.create(
                ingredient=get_object_or_404(Ingredient, id=id),
                recipe=instance, amount=amount
            )
        for tag in tags_data:
            instance.tags.add(tag)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return data  # noqa R504


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
