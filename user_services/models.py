from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model



User=get_user_model



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio=models.TextField(null=True,blank=True)
    profile_photo=models.ImageField(upload_to='profile_photos/', blank=True, null=True)


    @property
    def followers_count(self):
        return self.followers.count()
    


class NormalUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_photo=models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    # following = models.ManyToManyField(Teacher, related_name='followers')


    @property
    def following_count(self):
        return self.following.count()
    
    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    video_file=models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    

    @property
    def comment_count(self):
        return self.comments.count()
    
    @property
    def like_count(self):
        return self.likes.count()

    
    @property
    def liked_by_user(self):
        return [like.user for like in self.likes.all()]
    
    @property
    def files(self):
        return self.upload()


    def __str__(self) -> str:
        return self.title
    

#           i will comment ,like_count,liked_by_user and files propertys
        #   i will create like,comment,follow,file classes

class Like(models.Model):
    user = models.ForeignKey(
        NormalUser, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes'
    )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} liked {self.post}'

    class Meta:
        unique_together = ('user', 'post')


class Follow(models.Model):
    followers = models.ForeignKey(
        NormalUser, on_delete=models.CASCADE, related_name='followers'
    )
    followings = models.ForeignKey(
        NormalUser, on_delete=models.CASCADE, related_name='followings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.followers} followed by {self.followings}'

    class Meta:
        unique_together = ('followers', 'followings')


class Comment(models.Model):
    author=models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='author')
    definition=models.CharField(max_length=200)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_created=True)


    class Meta:
        ordering = ['create_at']


    def __str__(self) -> str:
        return f"{self.post} commented by {self.author}"


class Message(models.Model):
    author_message=models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_message')
    recipient=models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_message')
    content=models.TextField()
    sent_time=models.DateTimeField(auto_now_add=True)