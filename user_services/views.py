from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Teacher
from .serializers import TeacherSerializer
from .permissions import IsTeacherOrAdmin

class TeacherListCreateView(generics.ListCreateAPIView):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer
    permission_classes=[IsAuthenticated,IsTeacherOrAdmin]