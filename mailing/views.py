from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing


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


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        # фун-ция по созданию продукта только зарег. пользователям
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


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
    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailing/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


# CRUD для рассылки
class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")
