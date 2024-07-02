from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingParametersCreateView, MailingParametersListView, MailingParametersDetailView, \
    MailingParametersUpdateView, MailingParametersDeleteView, MessageListView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView, LogsListView, ManagerMailingParametersListView, index_data

app_name = MailingConfig.name

urlpatterns = [
    path('', index_data),
    path('list/', MailingParametersListView.as_view(), name='list'),
    path('create/', MailingParametersCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', MailingParametersDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', MailingParametersUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', MailingParametersDeleteView.as_view(), name='delete'),

    path('manager_list/', ManagerMailingParametersListView.as_view(), name='manager_list'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('logs_list/', LogsListView.as_view(), name='logs_list'),
]
