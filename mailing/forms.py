from django.forms import ModelForm

from mailing.models import MailingParameters


class MailingParametersForm(ModelForm):
    class Meta:
        model = MailingParameters
        exclude = ('creator',)


class MailingParametersManagerForm(ModelForm):
    class Meta:
        model = MailingParameters
        fields = ('status',)


class MailingForm(ModelForm):
    class Meta:
        model = MailingParameters
        exclude = ('creator',)
