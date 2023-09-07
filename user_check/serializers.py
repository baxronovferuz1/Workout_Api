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
from code_share.utils import phone_checker,phone_parser,send_phone_notification,send_email



# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     def __init__(self, *args, **kwargs):
#         super(MyTokenObtainPairSerializer, self).__init__(*args, **kwargs)
#         self.fields['userinput']=serializers.CharField(required=True)
#         self.fields['username']=serializers.CharField(read_only=True)


    # def auth_validate(self,attrs):
    #     user_input=attrs.get('userinput')
    #     if check_user_type(user_input)=='username':
    #         username=attrs.get('username')
    #     elif check_user_type(user_input)=='email':
    #         user=self.get_user(email__iexact=user_input)  #__iexact-"Baxronov@gmail.com" deb yozilgan email bazaga "baxronov@gmail.com" ko'rinishda bazga tushadi, custom emailni qayta kiritganda xato chiqmasligi ucun ishatiladi     
    #         username=user.username
    #     elif check_user_type(user_input)=='phone':
    #         user=self.get_user(phone_number=user_input)
    #         username=user.username
    #     else:
    #         data={
    #             'success':False,
    #             'message':'you must send phone number or email or username'
    #         }
    #         return ValidationError(data)
        
    #     authentication_kwargs={
    #         self.username_field:username,
    #         'password':attrs['password'] #userdan yuborilgan parol
    #     }

        


    #     current_user=User.objects.filter(username__iexact=username)  #filterni o'rniga get bo'lishi mumkin

    #     if current_user.auth_status!=DONE:
    #         raise ValidationError({'message':'you did not complete your authentication process'})
    #     user=authenticate(**authentication_kwargs)
    #     if user is not None:
    #         self.user=user
    #     else:
    #         raise ValidationError(
    #             {"password":"login or password you entered is incurrect,try again "}
    #         )


    # def auth_validate(self, attrs):
    #     user_input = attrs.get('userinput')
    #     password = attrs.get('password')
        
    #     if check_user_type(user_input) == 'username':
    #         username = attrs.get('userinput')  # Use the userinput field instead
    #     elif check_user_type(user_input) == 'email':
    #         user = self.get_user(email__iexact=user_input)
    #         username = user.username
    #     elif check_user_type(user_input) == 'phone':
    #         user = self.get_user(phone_number=user_input)
    #         username = user.username
    #     else:
    #         data = {
    #             'success': False,
    #             'message': 'you must send phone number or email or username'
    #         }
    #         raise serializers.ValidationError(data)
        
    #     authentication_kwargs = {
    #         self.username_field: username,
    #         'password': password
    #     }
        
    #     # return authentication_kwargs
    
    #     current_user=User.objects.filter(username__iexact=username)  #filterni o'rniga get bo'lishi mumkin

    #     if current_user.auth_status!=DONE:
    #         raise ValidationError({'message':'you did not complete your authentication process'})
    #     user=authenticate(**authentication_kwargs)
    #     if user is not None:
    #         self.user=user
    #     else:
    #         raise ValidationError(
    #             {"password":"login or password you entered is incurrect,try again "}
    #         )
    

    # def get_user(self, **kwargs):
    #     users=User.objects.filter(**kwargs)
    #     if not users.exists():
    #         raise exceptions.AuthenticationFailed(
    #             self.error_messages['no_active_account'],
    #             'no_active_account'
    #         )
    #     return users.first()







class SignUpSerializer(serializers.ModelSerializer):
    guid=serializers.UUIDField(read_only=True)



    def __init__(self, *args, **kwargs):
        super(SignUpSerializer,self).__init__(*args, **kwargs)
        self.fields['email_phone_number']=serializers.CharField(required=False)


    class Meta:
        model=User
        fields=(
            "guid",
            "auth_type",
            "auth_status"
        )

        extra_kwargs={
            "auth_type":{"read_only":True, "required":False},
            "auth_status":{'read_only':True, "required":False}
        }

    def create(self, validated_data):
        user=super(SignUpSerializer, self).create(validated_data)
        print(user)
        if user.auth_type==VIA_EMAIL:
            code=user.create_verify_code(user.auth_type)
            send_email(user.email, code)
        elif user.auth_type==VIA_PHONE:
            code=user.create_verify_code(user.auth_type)
            send_phone_notification(user.phone_number, code)




    def validate(self,in_data):
        super(SignUpSerializer,self).validate(in_data)
        data=self.auth_validate(in_data)
        return data




    @staticmethod
    def auth_validate(in_data):
        user_input=str(in_data.get('email_phone_number'))
        input_type=check_email_or_phone(user_input)
        if input_type=="email":
            data={
                "email":in_data.get("email_phone_number"),
                "auth_type":VIA_EMAIL
            }

        elif input_type=="phone":
            data={
                "email":in_data.get("email_phone_number"),
                "auth_type":VIA_PHONE
            }

        elif input_type is None:
            data={
                'success':False,
                'message':"you must send email_adress or phone number"
             
            }
            raise ValidationError(data)
        
        else:
            data={
                'success':False,
                "message":"you must send email_adress or phone number"
            }
            raise ValidationError(data)
        return data


    
    def validate_email_phone_number(self,value):
        value=value.lower()

        #Q-ketma-ket 5-6xil queryni yozish uchun mo'ljallangan

        query=(Q(phone_number=value) | Q(email=value)) & (
            Q(auth_status=NEW) | Q(auth_status=CODE_VERIFIED)
        )

        if User.objects.filter(query).exists():
            User.objects.get(query).delete()  #customer emailni yoki telefon raqamini kiritib 
                            # code kiritmasdan chiqib ketib qolsa,uni datalari bazaga saqlanmaydi yani DONE bo'lmagancha

        if value and User.objects.filter(email=value).exists():
            data = {
                "success": False,
                "message": "This Email address is already being used!"
            }
            raise ValidationError(data)

        elif value and User.objects.filter(phone_number=value).exists():
            data = {
                "success": False,
                "message": "This phone number is already being used!"
            }
            raise ValidationError(data)
        
        if check_email_or_phone(value) == "phone": #998931234567 shu ko'rinishda qabul qilinadi
            phone_parser(value )#,self.initial_data.get("country_code"))---agar country code berilgan bo'lsa shu qism ishlatiladi
            return value
            

           

    
