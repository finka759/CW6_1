from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from client.models import Client
from mailing.forms import MailingParametersManagerForm, MailingParametersForm
from mailing.models import MailingParameters, Message, Logs


class MailingParametersListView(ListView):
    model = MailingParameters

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        if self.request.user.is_authenticated:
            qs = qs.filter(creator=self.request.user)

        return qs


class ManagerMailingParametersListView(ListView):
    model = MailingParameters
    template_name = 'mailing_parameters_list.html'


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


def index_data(request):
    count_mailing_items = MailingParameters.objects.count()
    count_active_mailing_items = MailingParameters.objects.filter(status='is_active').count()
    count_unic_clients = Client.objects.values_list('email', flat=True).count()
    random_blogs = Blog.objects.order_by('?')[:3]
    context = {'count_mailing_items': count_mailing_items,
               'count_active_mailing_items': count_active_mailing_items,
               'count_unic_clients': count_unic_clients,
               'random_blogs': random_blogs,
               }

    return render(request, 'mailing/index.html', context)
