from django.urls import path
from projects.views import *

urlpatterns = [
  path('',index, name='projects.index'),

]
