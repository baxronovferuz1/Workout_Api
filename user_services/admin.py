from django.contrib import admin
from .models import Teacher,NormalUser,Post,Follow

admin.site.register(Teacher)
admin.site.register(NormalUser)
admin.site.register(Post)
admin.site.register(Follow)