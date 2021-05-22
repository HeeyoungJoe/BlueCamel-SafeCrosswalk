from django.urls import path
from django.contrib.auth import views as auth_view

from .views import *


urlpatterns=[
    path('user/',UserView,name='user_view'),
]
