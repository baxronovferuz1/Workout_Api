from django.urls import path
from .models import UserConfirmation



urlpatterns={
    path("", UserConfirmation),
}