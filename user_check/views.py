from django.shortcuts import render

# Create your views here.
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer