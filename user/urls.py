from django.urls import path
from user.views import *

urlpatterns = [
  # path('',index, name='projects.index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
