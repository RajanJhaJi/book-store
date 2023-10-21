from django.urls import path
from .views import register_user, login_user,logout_user

urlpatterns = [
    path('user/register',register_user),
    path('user/login',login_user),
    path('user/logout',logout_user)
]