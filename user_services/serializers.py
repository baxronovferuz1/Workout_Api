from rest_framework import serializers
from .models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'


class NormalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=NormalUser
        field='__all__'