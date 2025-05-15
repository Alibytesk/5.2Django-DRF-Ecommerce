#django
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db.models import Q
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
#dj verification
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
#apps
from .mixins import AnonymousMixin, LoginRequiredMixin
from .forms import *
#python
import hashlib
import requests
