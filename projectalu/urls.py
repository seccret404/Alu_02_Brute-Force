from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
     path('',views.awal,name='awal'),
     path('password',views.password,name='password')
]