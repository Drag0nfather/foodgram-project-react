from http import HTTPStatus

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer, ChangePasswordSerializer


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

    @action(methods=['post'],
            serializer_class=ChangePasswordSerializer,
            detail=False)
    def set_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(
                    serializer.data.get('current_password')):
                return Response({'current_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
            return Response({'status': 'password set'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
