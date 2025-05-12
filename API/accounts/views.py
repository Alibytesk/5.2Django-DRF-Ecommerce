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
#apps

class LoginAPIView(APIView):

    def post(self, request):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            jwt_token = AccessToken.for_user(user)
            return Response(data=dict({
                'jwt_token': str(jwt_token)
            }), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
