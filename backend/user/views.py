from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from user.handler import UserHandler
from user.models import User, Follow
from user.serializers import UserSerializer, ChangePasswordSerializer, SubscriptionSerializer, UserInputSerializer, \
    UserOutputSerializer


class UserViewSet(viewsets.ViewSet):
    """
    List all users or create a new user
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    user_handler = UserHandler()

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'],
            serializer_class=ChangePasswordSerializer,
            detail=False, permission_classes=[IsAuthenticated, IsAdminUser])
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

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(
            following__user=request.user).order_by('id')
        if queryset is not None:
            serializer = SubscriptionSerializer(
                queryset, many=True, context={'request': request})
            return Response(serializer.data)
        serializer = SubscriptionSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        followed = user.follower.filter(author=author).exists()
        if request.method == 'GET':
            if author != user and not followed:
                Follow.objects.create(user=user, author=author)
                serializer = UserSerializer(author,
                                            context={'request': request})
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            data = {'errors': 'Вы или уже подписаны на этого автора, или '
                              'пытаетесь подписаться на себя, что невозможно'}
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        if not user.follower.filter(author=author).exists():
            data = {'errors': 'Вы не подписаны на данного автора '
                              'напоминание: на себя подписаться невозможно)'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.filter(user=user, author=author).delete()
        data = {'deleted': 'success'}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    def create_user(self, request):
        data = request.data
        serializer = UserInputSerializer(data)
        user = self.user_handler.create_user(serializer.data)
        serialized_user = UserOutputSerializer(user)
        return Response(data=serialized_user.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = self.user_handler.list_user()
        serializer = UserSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = self.user_handler.get_user(pk)
        serializer = UserSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
