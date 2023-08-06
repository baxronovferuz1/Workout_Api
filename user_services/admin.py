from django.contrib import admin

# Register your models here.
from .views import TeacherListCreateView,TeacherDetailView

admin.site.register(TeacherListCreateView)