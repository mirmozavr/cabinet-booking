from django.urls import path
from aut.views import index, register_user, login_user, logout_user

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),
    path('', index)
]