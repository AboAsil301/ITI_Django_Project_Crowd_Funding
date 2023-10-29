from django.urls import path,include
from user.views import *
from . import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
  # path('',index, name='projects.index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('activation_instructions/', activation_instructions, name='activation_instructions'),
    path('activate/<str:token>/', activate, name='activate'),
    path('activation_success/', activation_success, name='activation_success'),
    path('activation_error/', activation_error, name='activation_error'),
    path('profile/<int:user_id>', profile, name='profile'),
    path('<int:pk>/edit', edit, name='edit'),
    path('<int:pk>/delete', delete, name='delete'),
    # path('', include('django.contrib.auth.urls')),
    # path('registration/login/', views.login, name='login'),

]
