from django.conf.urls import url
from rest_framework.authtoken import views

from user.utils.logout import Logout

urlpatterns = [
    url('auth/token/login/', views.obtain_auth_token),
    url(r'auth/token/logout/', Logout.as_view()),
]
