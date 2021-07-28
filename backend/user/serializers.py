from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
        model = User


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    model = User
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
