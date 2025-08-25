from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication, exceptions
import jwt
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .serializers import *
from django.contrib.auth import get_user_model
from .utils import *

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        session_persist = request.COOKIES.get('session_persist')
        session_id = request.COOKIES.get('session_id')
        print(session_id,'^^^^^^^^^^^^^^^ access')
        print(session_persist,'^^^^^^^^^^^^^^^ refresh')
        
        if not session_id:
            if not session_persist:
                raise AuthenticationFailed('No access token and refresh token not provided')
            return self.refresh_access_token(session_persist)

        try:
            payload = jwt.decode(session_id, settings.SECRET_KEY, algorithms=['HS256'])

            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
          
            return (user, None)

        except jwt.ExpiredSignatureError:
            if not session_persist:
                raise AuthenticationFailed('Refresh token not provided')
            return self.refresh_access_token(session_persist)

        except jwt.InvalidTokenError:
                raise AuthenticationFailed('Invalid refresh token')

        except user.DoesNotExist:
                raise AuthenticationFailed('User not found')

        
    def refresh_access_token(self, session_persist):
        try:
            payload_refresh = jwt.decode(session_persist, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload_refresh['user_id']
            user = User.objects.get(id=user_id)
        
            # Generate a new access token
            refresh = RefreshToken.for_user(user)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            response = Response({'session_id': new_access_token}, status=status.HTTP_200_OK)
         
            response.set_cookie(
                key='session_id',
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=5*60  
            )

            response.set_cookie(
                key='session_persist',
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=2*24*60 
            )

            return (user, None)
            # return(response)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Refresh token has expired')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid refresh token')

        except user.DoesNotExist:
            raise AuthenticationFailed('User not found') 




@api_view(['POST'])
def login(request):
    print(request.data)
    try:
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username, password=password)

                if user is None:
                    return Response({'error': ' Incorrect username or password'}, status=status.HTTP_404_NOT_FOUND)
               
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = Response({'message': 'Account Verified'}, status=status.HTTP_200_OK)

                response.set_cookie(
                    key='session_id',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age= 5*60  
                )

                response.set_cookie(
                    key='session_persist',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                     samesite='None',
                    max_age= 1*24*60*60
                )

                return response
        else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
            # Log the exception
            print(f'Error: {e}')
            return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CheckLoginStatus(APIView):
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAuthenticated]

     def get(self, request):
          user_obj = request.user
          print(user_obj)

          return Response('okay',status=status.HTTP_200_OK)


@api_view(['POST'])
def user_logout(request):
    return perform_logout(request)

