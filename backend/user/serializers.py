from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
        model = User
