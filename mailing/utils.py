from datetime import datetime

import pytz
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TIME_ZONE
from mailing.models import MailingAttempt, Mailing


def mailing_attempt(mailing_instance):
    """Отправляет письма клиентам и записывает результат."""
    try:
        # Отправляем письмо и получаем ответ сервера
        send_response = send_mail(
            subject=mailing_instance.message.subject,
            message=mailing_instance.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing_instance.clients.all()],
            fail_silently=False,
        )
        # Создаем отчет о рассылке с успешным статусом и ответом сервера
        MailingAttempt.objects.create(
            mailing=mailing_instance,
            status='success',
            server_response=send_response  # Ответ сервера
        )
    except Exception as e:
        # Неудачная попытка
        MailingAttempt.objects.create(
            mailing=mailing_instance,
            status='failed',
            server_response=str(e)
        )
        print(f"Ошибка при отправке рассылки: {e}")  # Выводим ошибку в консоль


def check_and_send_mailing():
    """Основная функция для проверки и отправки рассылок."""
    mailing_instances = Mailing.objects.all()

    for mailing_instance in mailing_instances:
        if mailing_instance.status == 'completed':
            continue

        process_mailing_status(mailing_instance)


def process_mailing_status(mailing_instance):
    """Обрабатывает статус рассылки."""
    if mailing_instance.status == 'created':
        mailing_attempt(mailing_instance)
        mailing_instance.status = 'started'
        mailing_instance.save()
        print('Рассылка начата.')
    elif mailing_instance.status == 'started':
        handle_started_mailing(mailing_instance)


def handle_started_mailing(mailing_instance):
    """Обрабатывает рассылку со статусом 'started'."""
    current_time = datetime.now(pytz.timezone(TIME_ZONE))
    last_attempt_instance = MailingAttempt.objects.filter(mailing=mailing_instance).order_by('-send_time').first()
    last_attempt_time = last_attempt_instance.send_time.astimezone(
        pytz.timezone(TIME_ZONE)) if last_attempt_instance else None

    if current_time > mailing_instance.actual_end_time:
        mailing_instance.status = 'completed'
        mailing_instance.save()
        print('Рассылка завершена.')
    else:
        check_periodicity_and_send(mailing_instance, current_time, last_attempt_time)


def check_periodicity_and_send(mailing_instance, current_time, last_attempt_time):
    """Проверяет периодичность и отправляет рассылку при необходимости."""
    if last_attempt_time is None:
        print("Невозможно определить время последней отправки.")
        return

    days_since_last_attempt = (current_time - last_attempt_time).days

    if mailing_instance.periodicity == 'monthly' and days_since_last_attempt >= 30:
        mailing_attempt(mailing_instance)
        print('Выполнена ежемесячная рассылка.')
    elif mailing_instance.periodicity == 'weekly' and days_since_last_attempt >= 7:
        mailing_attempt(mailing_instance)
        print('Выполнена еженедельная рассылка.')
    elif mailing_instance.periodicity == 'daily' and days_since_last_attempt >= 1:
        mailing_attempt(mailing_instance)
        print('Выполнена ежедневная рассылка.')
    else:
        print("Ничего не отправлено.")
