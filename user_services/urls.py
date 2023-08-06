from django.urls import path,include
from .views import TeacherListCreateView,TeacherDetailView,NormalUserDetailView,PostListCreateView,PostDetailView



urlpatterns=[
    path("teacher/",TeacherListCreateView.as_view()),
    path("learner/",NormalUserDetailView.as_view()),
    path("post/", PostListCreateView.as_view()),
]