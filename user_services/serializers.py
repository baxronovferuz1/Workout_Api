from rest_framework import serializers
from .models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'


class NormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=NormalUser
        fields='__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields=('id', 'user', 'post')

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Follow
        fields=('id', 'followers', 'followings')