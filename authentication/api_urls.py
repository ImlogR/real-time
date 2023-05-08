from django.urls import include, path
from .api_views import *

from rest_framework import routers

router= routers.DefaultRouter()

router.register(r'login', LoginViewSet, basename='login')
router.register(r'register', UserRegistrationViewset, basename='User')



urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', RegisterApi.as_view()),
    path('verify/', VerifyOTP.as_view()),
]
