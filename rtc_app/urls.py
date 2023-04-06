from django.urls import path
from .views import lobby

urlpatterns= [
    path('<str:group_name>/', lobby, name='lobby')
]