from django.urls import path

from mailing.views import index

app_name = "mailing"

urlpatterns = [
    path("", index),
]
