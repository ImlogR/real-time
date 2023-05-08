from django.urls import path
from .api_view import GroupListAPIView

# app_name = 'groups'

urlpatterns = [
    # path('create/', GroupCreateAPIView.as_view(), name='create'),
    path('list/', GroupListAPIView.as_view(), name='list'),
]