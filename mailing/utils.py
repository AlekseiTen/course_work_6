from datetime import datetime

import pytz
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TIME_ZONE
from mailing.models import MailingAttempt, Mailing


def mailing_attempt(mailing):
    """Отправляет письма клиентам и записывает результат."""
    try:
        # Отправляем письмо и получаем ответ сервера
        response = send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        # Создаем отчет о рассылке с успешным статусом и ответом сервера
        MailingAttempt.objects.create(
            mailing=mailing,
            status='success',
            server_response=response  # Ответ сервера
        )
    except Exception as e:
        # Неудачная попытка
        MailingAttempt.objects.create(
            mailing=mailing,
            status='failed',
            server_response=str(e)
        )
        print(f"Ошибка при отправке рассылки: {e}")  # Выводим ошибку в консоль


def check_and_send_mailing():
    """Основная функция для проверки и отправки рассылок."""

    # Получаем все объекты рассылок из базы данных
    mailing_objects = Mailing.objects.all()

    for mailing in mailing_objects:
        if mailing.status == 'completed':
            continue

        process_mailing_status(mailing)


def process_mailing_status(mailing):
    """Обрабатывает статус рассылки."""
    if mailing.status == 'created':
        mailing_attempt(mailing)
        mailing.status = 'started'
        mailing.save()
        print('Рассылка начата.')
    elif mailing.status == 'started':
        handle_started_mailing(mailing)


def handle_started_mailing(mailing):
    """Обрабатывает рассылку со статусом 'started'."""
    now = datetime.now(pytz.timezone(TIME_ZONE))
    last_attempt_object = MailingAttempt.objects.filter(mailing=mailing).order_by('-send_time').first()
    last_send_time = last_attempt_object.send_time.astimezone(
        pytz.timezone(TIME_ZONE)) if last_attempt_object else None

    if now > mailing.actual_end_time:
        mailing.status = 'completed'
        mailing.save()
        print('Рассылка завершена.')
    else:
        check_periodicity_and_send(mailing, now, last_send_time)


def check_periodicity_and_send(mailing, now, last_send_time):
    """Проверяет периодичность и отправляет рассылку при необходимости."""
    if last_send_time is None:
        print("Невозможно определить время последней отправки.")
        return

    days_since_last_send = (now - last_send_time).days

    if mailing.periodicity == 'monthly' and days_since_last_send >= 30:
        mailing_attempt(mailing)
        print('Выполнена ежемесячная рассылка.')
    elif mailing.periodicity == 'weekly' and days_since_last_send >= 7:
        mailing_attempt(mailing)
        print('Выполнена еженедельная рассылка.')
    elif mailing.periodicity == 'daily' and days_since_last_send >= 1:
        mailing_attempt(mailing)
        print('Выполнена ежедневная рассылка.')
    else:
        print("Ничего не отправлено.")
