from django.urls import path
from projects.views import *
from user.views import login
from django.contrib.auth import views as auth_views
urlpatterns = [
  path('',index, name='projects.index'),
  path('homepage', homepage, name='homepage'),
  path('projects/create/<int:user_id>', create_project, name='projects.create'),
  path('categories/create/', create_category, name='categories.create'),
  path('accounts/login/',login, name='login'),
  path('details/<int:project_id>', details, name='details'),
]
