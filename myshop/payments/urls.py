from django.urls import path
from .views import *

urlpatterns = [
    path('initkhalti/<int:id>',intikhalti,name='initkhalti'),
    path('verify/',verifyKhalti,name='verify'),
]
