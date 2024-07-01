from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailing.forms import MailingParametersManagerForm, MailingParametersForm
from mailing.models import MailingParameters, Message, Logs


class MailingParametersListView(ListView):
    model = MailingParameters


class MailingParametersDetailView(DetailView):
    model = MailingParameters


class MailingParametersCreateView(LoginRequiredMixin, CreateView):
    model = MailingParameters
    fields = ['name', 'mail', 'start_time', 'end_time', 'next_date', 'interval', 'status', 'client']
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        m_ps = form.save()
        m_ps.creator = self.request.user
        m_ps.save()
        return super().form_valid(form)


class MailingParametersUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingParameters
    fields = ['name', 'mail', 'start_time', 'end_time', 'next_date', 'interval', 'status', 'client']
    success_url = reverse_lazy('mailing:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.creator:
            return MailingParametersForm
        if user.has_perm('mailing.change_status'):
            return MailingParametersManagerForm
        raise PermissionDenied


class MailingParametersDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingParameters
    success_url = reverse_lazy('mailing:list')


class MessageListView(ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['theme', 'content', ]
    success_url = reverse_lazy('mailing:create')

    def form_valid(self, form):
        message = form.save()
        message.creator = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['theme', 'content', ]
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class LogsListView(ListView):
    model = Logs
