from django.urls import path
from .views import lobby, index, profile

urlpatterns= [
    path('', index, name='index'),
    path('accounts/profile/', profile, name='profile'),
    path('<slug:group_name>/', lobby, name='lobby')
]