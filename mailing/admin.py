from django.contrib import admin

from mailing.models import Message, MailingParameters


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'content')


@admin.register(MailingParameters)
class MailingParametersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mail', 'start_time', 'end_time', 'next_date', 'interval', 'status')
    search_fields = ('client', 'status')
    list_filter = ('client', 'status')
