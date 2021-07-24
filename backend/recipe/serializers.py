from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'colour', 'slug')
        model = Tag
