from django.urls import path

from mailing.views import index, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView

app_name = "mailing"

urlpatterns = [
    path("", index, name="index"),
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
]
