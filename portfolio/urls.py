from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('about/', AboutView.as_view(), name='about'),
]