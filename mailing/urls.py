from django.urls import path

from mailing.views import index, ClientListView, ClientCreateView

app_name = "mailing"

urlpatterns = [
    path("", index),
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
]
