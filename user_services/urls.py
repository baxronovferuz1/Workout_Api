from django.urls import path,include
# from .views import TeacherListCreateView,TeacherDetailView,NormalUserDetailView,PostListCreateView,PostDetailView,LikeDetailView,LikeListCreateView
from .views import *


urlpatterns=[
    path("teacher/",TeacherListCreateView.as_view()),
    path("learner/",NormalUserDetailView.as_view()),
    path("post/", PostListCreateView.as_view()),
    path("likes/",LikeListCreateView.as_view()),
    # path("likes/<int:pk>/", LikeDetailView.as_view())
    path("follow/",FollowListCreateView.as_view()),
    path("comment/", CommentListCreateView.as_view()),
    path("messages/",MessageViewSet.as_view()),
]

