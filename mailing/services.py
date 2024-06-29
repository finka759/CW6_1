import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingParameters, Message


def hello():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(hello, 'interval', seconds=30)
    scheduler.add_job(send_mailing, 'interval', seconds=10)
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
    # отправляем рассылку
    # получаем успешность(не успешность рассылки)
    # запись логов
    # проверка последнего дня рассылки, если наступил меняем статус на закончено
    # если послед день не наступил выставляем след дату
    for mailing in mailings:
        print('------')

        print('mailing.mail.theme')
        print(mailing.mail.theme)

        print('------')

        try:
            server_response = send_mail(
                subject=mailing.mail.theme,
                message=mailing.mail.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.client.all()],
                fail_silently=False
            )
            print('server_response')
            print(server_response)
            print('------')
            server_respons = 'ok'
            status = True
        except smtplib.SMTPException as e:
            server_respons = str(e)
            status = False

        # if status:
        #     mailing.logs.create(status='success', response='рассылка отправлена успешно')
        #     mailing.next_date = mailing.start_time + mailing.interval
        #     if mailing.next_date < current_datetime:
        #         mailing.next_date = current_datetime + mailing.interval
        #     mailing.save()
