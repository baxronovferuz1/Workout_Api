from django.shortcuts import render

# Create your views here.
# from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import SignUpSerializer
from rest_framework import permissions,status
from rest_framework.generics import CreateAPIView

# class LoginView(TokenObtainPairView):
#     serializer_class=MyTokenObtainPairSerializer



class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer