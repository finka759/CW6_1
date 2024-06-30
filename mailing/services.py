import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import MailingParameters, Message, Logs


def hello():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()


# Главная функция по отправке рассылки
def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    # проверка статуса активных рассылок  и если дата завершения прошла меняем статус на завершенную
    print('начало проверки дат окончания активных рассылок')
    for mailing in MailingParameters.objects.all():
        if mailing.end_time < current_datetime and mailing.status == 'is_active':
            mailing.status = ['finished_date']
            mailing.save()
    print('конец проверки дат окончания активных рассылок')

    # создание объекта с применением фильтра
    mailings = (
        MailingParameters.objects.filter(start_time__lte=current_datetime).filter(status__in=['is_active']).filter(
            next_date__lte=current_datetime))

    for mailing in mailings:

        rl = [client_.email for client_ in mailing.client.all()]
        server_response = ''
        status = False
        try:
            server_response = send_mail(
                subject=mailing.mail.theme,
                message=mailing.mail.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=rl,
                fail_silently=False
            )
            print('server_response')
            print(server_response)
            server_response = str(server_response)
            status = True
        except smtplib.SMTPException as e:
            server_response = str(e)
            status = False
        finally:
            log = Logs(status=status, response=server_response, last_time_sending=current_datetime,
                       mailing_parameters=mailing)
            print(log)
            log.save()

            next_date_calculated = None
            # получаем следующий расчетный день рассылки
            if mailing.interval == 'per_day':
                next_date_calculated = mailing.next_date + timezone.timedelta(days=1)
            elif mailing.interval == 'per_week':
                next_date_calculated = mailing.next_date + timezone.timedelta(days=7)
            elif mailing.interval == 'per_month':
                next_date_calculated = mailing.next_date + timezone.timedelta(days=30)

            if next_date_calculated > mailing.end_time:
                if status:
                    mailing.status = 'finished'
                else:
                    mailing.status = 'finished_error'
            else:
                mailing.next_date = next_date_calculated

            mailing.save()
