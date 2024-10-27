from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm
from mailing.models import Client


def index(request):
    return render(request, 'mailing/base.html')


# CRUD для клиентов
class ClientListView(ListView):
    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"


class ClientDetailView(DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")


# CRUD для сообщений
class MessageListView(ListView):
    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"


class MessageDetailView(DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class MessageCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class MessageUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class MessageDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")


# CRUD для рассылки
class MailingListView(ListView):
    model = Client
    template_name = "mailing/client_list.html"
    context_object_name = "clients"


class MailingDetailView(DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class MailingCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class MailingUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")


class MailingDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:client_list")
