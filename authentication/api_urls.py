from django.urls import include, path
from .api_views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers

router= routers.DefaultRouter()

router.register(r'login', LoginViewSet, basename='login')
router.register(r'register', UserRegistrationViewset, basename='User')


urlpatterns = [    ]


urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', RegisterApi.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
