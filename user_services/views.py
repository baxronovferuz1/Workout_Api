from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Teacher,NormalUser,Post,Like,Follow
from .serializers import TeacherSerializer,NormalUserSerializer,PostSerializer,LikeSerializer,FollowSerializer
from .permissions import IsTeacherOrAdmin,IsNormalUser

class TeacherListCreateView(generics.ListCreateAPIView):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer
    permission_classes=[IsAuthenticated,IsTeacherOrAdmin]




class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Teacher.objects.all()
    serializer_class=TeacherSerializer
    permission_classes=[IsAuthenticated,IsTeacherOrAdmin]





class NormalUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=NormalUser.objects.all()
    serializer_class=NormalUserSerializer
    permission_classes=[IsAuthenticated,IsNormalUser]




class PostListCreateView(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated,IsTeacherOrAdmin]




class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated,IsTeacherOrAdmin]




class LikeListCreateView(generics.ListCreateAPIView):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    permission_classes=[IsAuthenticated]



class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    permission_classes=[IsAuthenticated]



class FollowListCreateView(generics.ListCreateAPIView):
    queryset=Follow.objects.all()
    serializer_class=FollowSerializer
    permission_classes=[IsAuthenticated]

class FollowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Follow.objects.all()
    serializer_class=FollowSerializer
    permission_classes=[IsAuthenticated]


    
