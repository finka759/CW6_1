from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from mailing.models import MailingParameters


# def index(request):
#     return render(request, 'mailing/base.html')


class MailingParametersListView(ListView):
    model = MailingParameters


class MailingParametersDetailView(DetailView):
    model = MailingParameters


class MailingParametersCreateView(CreateView):
    model = MailingParameters
    fields = ['name', 'mail', 'start_time', 'end_time', 'next_date', 'is_active', 'interval']
    success_url = reverse_lazy('mailing:list')


class MailingParametersUpdateView(UpdateView):
    model = MailingParameters
    fields = ['name', 'mail', 'start_time', 'end_time', 'next_date', 'is_active', 'interval']
    success_url = reverse_lazy('mailing:list')
