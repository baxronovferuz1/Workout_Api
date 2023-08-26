from datetime import datetime,timedelta #timedeltani vaqt qoshishda ishlatamiz
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,UserManager
from django.core.validators import RegexValidator
import uuid
from django.conf import settings
import random
from rest_framework_simplejwt.tokens import RefreshToken

ORDINARY_USER, TEACHER, SUPER_ADMIN = (
    'ordinary_user',
    'teacher', 
    'super_admin'
)

VIA_EMAIL,VIA_PHONE,VIA_USERNAME=(
    "via_email",
    "via_phone",
    "via_username"
)


# MALE,FEMALE=(
#     "male",
#     "femail"
# )


NEW,CODE_VERIFIED,DONE=(
    "NEW",
    "CODE_VERIFIED",
    "DONE"
)
PHONE_EXPIRE=2
EMAIL_EXPIRE=5

class UserConfirmation(models.Model):
    TYPE_CHOICES=(
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )

    code=models.CharField(max_length=4)
    user=models.ForeignKey('users.User',on_delete=models.CASCADE, related_name='verify_codes')
    verify_type=models.CharField(max_length=31, choices=TYPE_CHOICES)
    expiration_time=models.DateTimeField(null=True) #yuborilgan codeni tugash vaqti
    is_confirmed=models.BooleanField(default=False)  #tasdiqlandi✔️



    def __str__(self):
        return str(self.user.__str__())

    
    def save(self,*args,**kwargs):
        if not self.pk:
            if self.verify_type==VIA_EMAIL:
                self.expiration_time=datetime.now()+timedelta(minutes=EMAIL_EXPIRE)

            else:
                self.expiration_time=datetime.now()+timedelta(minutes=PHONE_EXPIRE)
            
        super(UserConfirmation, self).save(*args,**kwargs)




class User(AbstractUser):
    _validate_phone=RegexValidator(
        regex=r"^9\d{12}$",
        message='Your phone number should start with 9 and have 12 digits',
    )

    USER_ROLES=(
        (ORDINARY_USER, ORDINARY_USER),
        (TEACHER,TEACHER),
        (SUPER_ADMIN,SUPER_ADMIN)    
    )
    AUTH_TYPE_CHOICES=(
        (VIA_EMAIL,VIA_EMAIL),
        (VIA_PHONE,VIA_PHONE),
        (VIA_USERNAME,VIA_USERNAME)
    )

    #Qaysi pagedaligini aniqlaydi
    AUTH_STATUS=(
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED)

    )
    

    
    user_roles=models.CharField(max_length=31,choices=USER_ROLES, default=ORDINARY_USER)
    auht_type=models.CharField(max_length=35, choices=AUTH_TYPE_CHOICES, default=VIA_USERNAME)
    auht_status=models.CharField(max_length=35, choices=AUTH_STATUS, default=NEW)
    email=models.EmailField(null=True,unique=True)
    phone_number=models.CharField(max_length=12,null=True, blank=True,unique=True,validators=[_validate_phone])
    bio=models.CharField(max_length=200,blank=True,null=True)
    
    object=UserManager()

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self,verify_type):
        code="".join(str(random.randint(1000,9999)))
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code 
    

    def check_username(self):
        if not self.username:
            temporary_username=f"user_project-{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username=temporary_username):
                temporary_username=f"{temporary_username}{random.randint(0,9)}"
            self.username=temporary_username



    def check_email(self):
        if self.email:
            normalized_email=self.email.lower()
            self.email=normalized_email


    def check_password(self):
        if not self.password:
            temporary_password=f"password{uuid.uuid4().__str__().split('-')[-1]}"
            self.password=temporary_password


    def hashing_password(self):
        if not self.password.startswith('pgjrf5_gdgd415'): #startswith() usuli satrning belgilangan pastki qatordan boshlanishini tekshiradi
            self.set_password(self.password)
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        }
    

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_password()
        self.hashing_password()



    def save(self, *args, **kwargs):

        if not self.pk:
            self.clean()
        super(User, self).save(*args, **kwargs)
