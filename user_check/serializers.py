from abc import ABC
from rest_framework import serializers
from user_check.models import User,UserConfirmation
from user_check.models import VIA_EMAIL,VIA_PHONE
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from user_check.models import CODE_VERIFIED,DONE,NEW
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from workout_api.utility import check_user_type
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