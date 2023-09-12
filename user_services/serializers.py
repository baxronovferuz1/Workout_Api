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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['author','definition','create_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields=('id','author_message','recipient','content','sent_time')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=('post','file')