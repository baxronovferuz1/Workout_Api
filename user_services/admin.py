from django.contrib import admin

# Register your models here.
from .models import Teacher,NormalUser

admin.site.register(Teacher)
admin.site.register(NormalUser)