from django.db import models
from django.utils import timezone

from client.models import Client
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    theme = models.CharField(
        max_length=150,
        verbose_name='тема письма',
        **NULLABLE
    )
    content = models.TextField(
        verbose_name='содержимое письма'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='cоздатель',
        **NULLABLE,
    )

    def __str__(self):
        return f'{self.theme} {self.content}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class MailingParameters(models.Model):
    intervals = (
        ('per_day', 'раз в день'),
        ('per_week', 'раз в неделю'),
        ('per_month', 'раз в месяц')
    )
    status_variants = (
        ('not_active', 'не активна'),
        ('is_active', 'запущена'),
        ('finished', 'закончена успешно'),
        ('finished_date', 'закончена по сроку'),
        ('finished_error', 'законечена с ошибками')
    )
    name = models.CharField(
        verbose_name="название рассылки",
        max_length=50,
        default='mailing_no_name'
    )
    client = models.ManyToManyField(
        Client,
        verbose_name='получатель'
    )
    mail = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='начало рассылки'
    )
    end_time = models.DateTimeField(
        default=(timezone.now() + timezone.timedelta(days=1)),
        verbose_name='конец рассылки'
    )
    next_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='дата следующей рассылки'
    )
    interval = models.CharField(
        default='per_day',
        max_length=50,
        choices=intervals,
        verbose_name="интервал рассылки"
    )
    status = models.CharField(
        max_length=50,
        choices=status_variants,
        default='not_active',
        verbose_name='Статус рассылки'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='cоздатель',
        **NULLABLE,
    )

    def __str__(self):
        return (f'{self.name}: ({self.start_time} - {self.end_time};интервал:{self.interval};'
                f' статус:{self.status}), creator:{self.creator}')

    class Meta:
        verbose_name = 'настройка рассылки'
        verbose_name_plural = 'настройки рассылок'
        permissions = [
            ('change_status', 'Can change status'),
        ]


class Logs(models.Model):
    mailing_parameters = models.ForeignKey(MailingParameters, on_delete=models.CASCADE,
                                           verbose_name='параметры_рассылки')
    last_time_sending = models.DateTimeField(auto_now=True, verbose_name='время последней рассылки', **NULLABLE)
    status = models.CharField(max_length=50, verbose_name='статус попытки', **NULLABLE)
    response = models.CharField(max_length=200, verbose_name="ответ почтового сервера", **NULLABLE)

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

    def __str__(self):
        return f'''Отправлено: {self.last_time_sending},
                  'Статус: {self.status} ,
                  'Response: {self.response},
                  'Mailing_parameters: {self.mailing_parameters}'''
