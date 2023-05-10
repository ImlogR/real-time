from rest_framework import viewsets
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer, VerifyAccountSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from .emails import send_otp_via_email
from rest_framework_simplejwt.tokens import RefreshToken




def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class RegisterApi(APIView):
    def post(self, request):
        try:
            data= request.data
            serializer= UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(email=serializer.data['email'])
                return Response({
                    'status':200,
                    'message': 'Registration Successful check email!',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)

class VerifyOTP(APIView):
    def post(self, request):
        try:
            data= request.data
            serializer= VerifyAccountSerializer(data= data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp= serializer.data['otp']
                user= CustomUser.objects.filter(email= email)
                if not user.exists:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'invalid email`'
                    })
                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'invalid otp`'
                    })
                user= user.first()
                user.is_verified= True
                user.save()

                return Response({
                    'status':200,
                    'message': 'Account Verified!!',
                    'data': serializer.data
                })
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': 'server error'
            })

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
        send_otp_via_email(email=user.email)
        return Response({'msg':'Registration succesful!! Check email to Verify!!'}, status=status.HTTP_201_CREATED)
    
class LoginViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    
   
    def list(self, request, *args, **kwargs):
        return Response({"error":"login_required"})
    

    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        # user= CustomUser.objects.get(email=email)

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
            return Response({'error': 'Accouunt is not verified yet'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # login(request, user)
            token = get_tokens_for_user(user)

            return Response({'token':token,'msg':f'Login Successful', 'user':user.email}, status=status.HTTP_200_OK)