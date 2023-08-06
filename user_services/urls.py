from django.urls import path,include
from .views import TeacherListCreateView,TeacherDetailView,NormalUserListCreateView,NormalUserDetailView



urlpatterns=[
    path("teacher/",TeacherListCreateView.as_view()),
    path("learner/",NormalUserListCreateView.as_view()),
]