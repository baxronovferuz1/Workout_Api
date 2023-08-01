from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import uuid



# class TimeStamp(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     time_stamp=models.DateTimeField(auto_now=True)
#     created_time=models.DateField(auto_now_add=True)

#     class Meta:
#         abstract=True


class User(AbstractUser):
    #for change password
    #current_password=models.CharField(max_length=100, null=True)
    #new_password=models.CharField(max_length=100, null=True) """


    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.followings.count()    

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'
