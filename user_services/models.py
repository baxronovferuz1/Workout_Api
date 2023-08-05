from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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


    @property
    def followers_count(self):
        return self.followers.count()
    


class NormalUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # following = models.ManyToManyField(Teacher, related_name='followers')


    @property
    def following_count(self):
        return self.following.count()
    
    def __str__(self):
        return self.username

class Post(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    video_file=models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

