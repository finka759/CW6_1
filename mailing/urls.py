from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingParametersCreateView, MailingParametersListView, MailingParametersDetailView, \
    MailingParametersUpdateView

app_name = MailingConfig.name

urlpatterns = [
    path('mailingparameters_list/', MailingParametersListView.as_view(), name='mp_list'),
    path('', MailingParametersListView.as_view(), name='mp_list'),
    path('create/', MailingParametersCreateView.as_view(), name='create'),
    path('mp_detail/<int:pk>/',  MailingParametersDetailView.as_view(), name='mp_detail'),
    path('edit/<int:pk>/', MailingParametersUpdateView.as_view(), name='edit'),
    # path('create/', Client___View.as_view(), name='delete'),
]