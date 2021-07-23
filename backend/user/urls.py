from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from user.utils.logout import Logout
from user.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/token/login/', views.obtain_auth_token),
    path('auth/token/logout/', Logout.as_view()),
    path('', include(router.urls))
]
