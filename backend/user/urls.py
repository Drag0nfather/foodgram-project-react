from django.urls import path, re_path
from rest_framework.authtoken import views

from user.utils.logout import Logout
from user.views import UserViewSet


urlpatterns = [
    path('auth/token/login/', views.obtain_auth_token),
    path('auth/token/logout/', Logout.as_view()),
    re_path(r'^auth/users/$', UserViewSet.as_view({'post': 'create_user'})),
    re_path(r'^users/$', UserViewSet.as_view({'get': 'list'})),
    re_path(r'^users/(?P<pk>[0-9]+)/$', UserViewSet.as_view({'get': 'retrieve'})),
    re_path(r'^users/set_password/$', UserViewSet.as_view({'post': 'set_password'})),
    re_path(r'^users/subscriptions/$', UserViewSet.as_view({'get': 'subscriptions'})),
    re_path(r'^users/(?P<pk>[0-9]+)/subscribe/$', UserViewSet.as_view({'get': 'subscribe', 'delete': 'subscribe'})),
]
