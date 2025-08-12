from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, CustomTokenSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_simplejwt import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from django.conf import settings
from resto.models import User

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainView(views.TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request: views.Request, *args, **kwargs) -> views.Response:

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        request_data = request.data
        user = User.objects.get(email = request_data['email'])

        response = Response({
            'is_admin' : data['is_admin'], 
            'is_staff' : data['is_staff'], 
            'access' : data['access'], 
            'role' : user.role, 
            'user_id' : user.id, 
            'username' : f'{user.first_name} {user.last_name}'
        })

        response.set_cookie('access', data['access'], samesite='None', secure=True, httponly=True)

        return response
    
# @api_view(['GET'])
# def verify_tokens(request):
#     if request.method == 'GET':
#         print('Event')
    
#     return Response({'error' : "Invalid Request"}, status=status.HTTP_200_OK)

class VerifyToken(APIView):

    def get(self, request: views.Request, *args, **kwargs) -> Response:
        try:
            token = request.COOKIES.get('access')
            if not token:
                return Response({'msg' : "Unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)
            UntypedToken(token)


            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # decoded_data = TokenBackend(algorithm='HS256')
            # decoded_data = decoded_data.decode(token, verify=True)
            user = User.objects.filter(id = decoded_data["user_id"]).first
            if not user:
                return Response({'msg' : "Unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)

            response = {
                'is_admin' : decoded_data['is_superuser'], 
                'is_staff' : decoded_data['is_staff']
            }

            return Response(response, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'msg' : "Unauthorised"}, status=status.HTTP_401_UNAUTHORIZED)
            
    

