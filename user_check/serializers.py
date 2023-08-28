from abc import ABC
from rest_framework import serializers
from .models import User,UserConfirmation
from .models import VIA_EMAIL,VIA_PHONE
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CODE_VERIFIED,DONE,NEW
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from workout_api.utility import check_user_type,check_email_or_phone
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super(MyTokenObtainPairSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput']=serializers.CharField(required=True)
        self.fields['username']=serializers.CharField(read_only=True)


    def auth_validate(self,attrs):
        user_input=attrs.get('userinput')
        if check_user_type(user_input)=='username':
            username=attrs.get('username')
        elif check_user_type(user_input)=='email':
            user=self.get_user(email__iexact=user_input)  #__iexact-"Baxronov@gmail.com" deb yozilgan email bazaga "baxronov@gmail.com" ko'rinishda bazga tushadi, custom emailni qayta kiritganda xato chiqmasligi ucun ishatiladi     
            username=user.username
        elif check_user_type(user_input)=='phone':
            user=self.get_user(phone_number=user_input)
            username=user.username
        else:
            data={
                'success':False,
                'message':'you must send phone number or email or username'
            }
            return ValidationError(data)
        
        authentication_kwargs={
            self.username_field:username,'password':attrs['password'] #userdan yuborilgan parol
        }

        


        current_user=User.objects.filter(username__iexact=username)  #filterni o'rniga get bo'lishi mumkin

        if current_user.auth_status!=DONE:
            raise ValidationError({'message':'you did not complete your authentication process'})
        user=authenticate(**authentication_kwargs)
        if user is not None:
            self.user=user
        else:
            raise ValidationError(
                {"password":"login or password you entered is incurrect,try again "}
            )