from datetime import datetime

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingAttempt


# def print_time_job():
#     #time_zone = pytz.timezone(settings.TIME_ZONE)
#     now = datetime.now()
#     print(f"Текущее время: {now}")


def send_mailing():
    now = timezone.now()
    current_datetime = now.astimezone(pytz.timezone(settings.TIME_ZONE))
    mailings = get_mailings_to_send(current_datetime)

    for mailing in mailings:

        if can_send_mailing(mailing):
            send_mailing_to_clients(mailing)
        print(f"Текущая рассылка: {mailing}")


def get_mailings_to_send(current_datetime):
    """Получает все рассылки, которые нужно отправить."""
    return Mailing.objects.filter(start_time__lte=current_datetime)


def can_send_mailing(mailing):
    """Проверяет, можно ли отправить данную рассылку."""
    last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-send_time').first()
    # print(last_attempt)

    if last_attempt:
        time_since_last_attempt = (timezone.now() - last_attempt.send_time).days
        if mailing.periodicity == 'daily' and time_since_last_attempt < 1:
            return False  # Не отправляем, если последняя попытка была менее суток назад

    return True  # Можно отправить


def send_mailing_to_clients(mailing):
    """Отправляет письма клиентам и записывает результат."""
    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        log_attempt(mailing, 'success')
        mailing.status = 'started' if mailing.status == 'created' else mailing.status
    except Exception as e:
        log_attempt(mailing, 'failed', str(e))


def log_attempt(mailing, status):
    """Записывает попытку рассылки в базу данных."""
    MailingAttempt.objects.create(
        mailing=mailing,
        status=status,
    )
