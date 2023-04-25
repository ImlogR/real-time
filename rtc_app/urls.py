from django.urls import path
from .views import lobby, index

urlpatterns= [
    path('', index, name='index'),
    path('<slug:group_name>/', lobby, name='lobby')
]