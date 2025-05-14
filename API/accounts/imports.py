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
from django.utils.crypto import get_random_string
#apps
from .models import *

from random import randint as rnd