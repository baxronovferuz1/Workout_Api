from django.urls import path,include
from .views import TeacherListCreateView,TeacherDetailView



urlpatterns=[
    path("teacher/",TeacherListCreateView.as_view()),
]