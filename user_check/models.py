# from django.db import models

# # Create your models here.
# from datetime import datetime,timedelta #timedeltani vaqt qoshishda ishlatamiz
# from django.db import models
# from django.contrib.auth.models import AbstractUser,AbstractBaseUser,UserManager
# from django.core.validators import RegexValidator
# import random
# from rest_framework_simplejwt.tokens import RefreshToken
# import uuid



# ORDINARY_USER, MANAGER, SUPER_ADMIN = (
#     'ordinary_user',
#     'manager',
#     'super_admin'
# )

# VIA_EMAIL,VIA_PHONE,VIA_USERNAME=(
#     "via_email",
#     "via_phone",
#     "via_username"
# )


# MALE,FEMALE=(
#     "male",
#     "femail"
# )


# NEW,CODE_VERIFIED,DONE=(
#     "NEW",
#     "CODE_VERIFIED",
#     "DONE"
# )
# PHONE_EXPIRE=2
# EMAIL_EXPIRE=5

# class UserConfirmation(models.Model):
#     TYPE_CHOICES=(
#         (VIA_PHONE, VIA_PHONE),
#         (VIA_EMAIL, VIA_EMAIL)
#     )

#     code=models.CharField(max_length=4)
#     user=models.ForeignKey('users.User',on_delete=models.CASCADE, related_name='verify_codes')
#     verify_type=models.CharField(max_length=31, choices=TYPE_CHOICES)
#     expiration_time=models.DateTimeField(null=True) #yuborilgan codeni tugash vaqti
#     is_confirmed=models.BooleanField(default=False)  #tasdiqlandi✔️



#     def __str__(self):
#         return str(self.user.__str__())

    
#     def save(self,*args,**kwargs):
#         if not self.pk:
#             if self.verify_type==VIA_EMAIL:
#                 self.expiration_time=datetime.now()+timedelta(minutes=EMAIL_EXPIRE)

#             else:
#                 self.expiration_time=datetime.now()+timedelta(minutes=PHONE_EXPIRE)
            
#         super(UserConfirmation, self).save(*args,**kwargs)
