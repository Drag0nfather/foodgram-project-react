from typing import Dict

from django.shortcuts import get_object_or_404

from user.models import User


class UserHandler:
    @staticmethod
    def create_user(data: Dict):
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        return user

    def list_user(self):
        users = User.objects.all()
        return users

    def get_user(self, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        return user
