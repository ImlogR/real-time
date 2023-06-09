from rest_framework import viewsets
# from .serializers import UserLoginSerializer, UserRegistrationSerializer
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login


class UserRegistrationViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    
# class LoginViewSet(viewsets.ModelViewSet):
    
#     queryset = CustomUser.objects.all()
#     serializer_class = UserLoginSerializer
#     permission_classes = [AllowAny]

    
   
#     def list(self, request, *args, **kwargs):
#         return Response({"error":"login_required"})
    

#     def create(self, request, *args, **kwargs):
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']

#         user = authenticate(request, email=email, password=password)
#         if user is None:
#             return Response({'error': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)

#         login(request, user)

#         return Response({'msg':f'Login Success', 'user':user.email}, status=status.HTTP_200_OK)