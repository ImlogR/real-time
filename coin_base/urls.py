from django.urls import path
from .views import create_coins

urlpatterns= [
    path('coin-create', create_coins, name='coin_creator')
]
