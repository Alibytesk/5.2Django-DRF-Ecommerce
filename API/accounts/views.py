#restJWT
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
#restApi
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
#django
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.db.models import Q
#apps
from .models import *




class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            jwt_token = AccessToken.for_user(user)
            return Response(data=dict({
                'jwt_token': str(jwt_token)
            }), status=status.HTTP_200_OK)
        else:
            username = data.get('username')
            if User.objects.filter(
                Q(username__exact=username) |
                Q(phone__exact=username)    |
                Q(email__exact=username)
            ).exists():
                return Response(data={'response': 'incorrect password'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'response': 'please enter a valid username, phone or email'},
                            status=status.HTTP_400_BAD_REQUEST)


class AuthenticateCheckAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response(data={'response':'is_Authenticated'}, status=status.HTTP_200_OK)