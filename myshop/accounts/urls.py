from django.urls import path
from .views import *

urlpatterns = [
 path('login/',log_in,name='login'),
 path('register/',register,name='register'),
 path('logout/',log_out,name='logout'),
 path('profile/',profile,name='profile'),
 path('dashboard/',dashboard,name='dashboard'), 
 path('myorder/',myorder,name='myorder')
]


