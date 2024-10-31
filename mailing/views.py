from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Message, Mailing


class MainPage(View):
    """Выводит статистику"""
    def get(self, request, *args, **kwargs):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status="started").count()
        unique_clients_count = Client.objects.distinct().count()

        context = {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_clients_count": unique_clients_count,
        }

        return render(request, "mailing/index.html", context)


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
        # фун-ция по созданию клиента только авторизаванных пользователей
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


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        # фун-ция по созданию сообщения только авторизаванных пользователей
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


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


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        # фун-ция по созданию рассылки только авторизаванных пользователей
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")
