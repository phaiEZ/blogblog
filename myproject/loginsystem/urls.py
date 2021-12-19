from django.urls import path
from .views import index, login, logout, register
urlpatterns = [
    path('register', index, name="member"),
    path('register/add', register, name="addUser"),
    path('login', login, name="login"),
    path('logout', logout, name="logout")
]
# name = name of this url
# /user/register
