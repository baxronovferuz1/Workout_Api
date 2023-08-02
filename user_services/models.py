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
        

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def liked_by_users(self):
        return [like.user for like in self.likes.all()]
    
    def __str__(self):
        return self.title
    
    @property
    def files(self):
        return self.upload()
