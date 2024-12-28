from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('about/', AboutView.as_view(), name='about'),
    path('credentials/', CredentialsView.as_view(), name='credentials'),
    path('works/', WorksView.as_view(), name='works'),
    path('works/<slug:slug>/', WorkDetailView.as_view(), name='work_detail'),
]