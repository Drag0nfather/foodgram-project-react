from http import HTTPStatus

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    List all users or create a new user
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['get'], detail=False)
    def me(self, request):
        if self.request.user is None:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        if self.request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=HTTPStatus.UNAUTHORIZED)
