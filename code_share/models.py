from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    guid=models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)


    class Meta:
        abstract=True
