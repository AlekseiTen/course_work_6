from datetime import datetime
import pytz
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER, TIME_ZONE
from mailing.models import Mailing, MailingAttempt


def mailing_attempt(mailing):
    """Отправляет письма клиентам и записывает результат."""
    try:
        # Отправляем письмо и получаем ответ сервера
        response = send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()],  # Список адресов получателей
            fail_silently=False,  # Если произойдет ошибка, выбрасываем исключение
        )
        # Создаем отчет о рассылке с успешным статусом и ответом сервера
        MailingAttempt.objects.create(
            mailing=mailing,  # Связываем отчет с конкретной рассылкой
            status='success',  # Указываем статус успешной попытки
            server_response=response  # Сохраняем ответ сервера
        )
    except Exception as e:
        # Неудачная попытка отправки письма
        MailingAttempt.objects.create(
            mailing=mailing,  # Связываем отчет с конкретной рассылкой
            status='failed',  # Указываем статус неудачной попытки
            server_response=str(e)  # Сохраняем текст ошибки как ответ сервера
        )
        print(f"Ошибка при отправке рассылки: {e}")  # Выводим ошибку в консоль


def check_and_send_mailing():
    """Основная функция для проверки и отправки рассылок."""

    # Получаем все объекты рассылок из базы данных
    mailing_object = Mailing.objects.all()

    for mailing in mailing_object:  # Проходим по всем объектам рассылок
        if mailing.status == 'completed':  # Если рассылка завершена, пропускаем ее
            continue
        elif mailing.status == 'created':  # Если рассылка только создана
            mailing_attempt(mailing)  # Пытаемся отправить письма
            mailing.status = 'started'  # Меняем статус на "начата"
            mailing.save()  # Сохраняем изменения в базе данных

        elif mailing.status == 'started':  # Если рассылка уже начата
            now = datetime.now(pytz.timezone(TIME_ZONE))  # Получаем текущее время в заданном часовом поясе

            last_attempt_object = MailingAttempt.objects.filter(mailing=mailing).order_by('-send_time').first()
            # Получаем последнюю попытку отправки этой рассылки, отсортированную по времени отправки

            last_send_time = last_attempt_object.send_time.astimezone(
                pytz.timezone(TIME_ZONE)) if last_attempt_object else None
            # Преобразуем время последней попытки в заданный часовой пояс (если такая попытка была)

            if now > mailing.actual_end_time:  # Если текущее время больше времени окончания рассылки
                mailing.status = 'completed'  # Меняем статус на "завершена"
                mailing.save()  # Сохраняем изменения в базе данных
                print('рассылка завершена')  # Выводим сообщение о завершении

            elif mailing.periodicity == 'monthly' and (now - last_send_time).days >= 30:
                # Если периодичность ежемесячная и прошло больше или равно 30 дней с последней попытки
                mailing_attempt(mailing)  # Пытаемся снова отправить письма
                print('выполнена ежемесячная рассылка')

            elif mailing.periodicity == 'weekly' and (now - last_send_time).days >= 7:
                # Если периодичность еженедельная и прошло больше или равно 7 дней с последней попытки
                mailing_attempt(mailing)
                print('выполнена еженедельная рассылка')

            elif mailing.periodicity == 'daily' and (now - last_send_time).days >= 1:
                # Если периодичность ежедневная и прошло больше или равно одного дня с последней попытки
                mailing_attempt(mailing)
                print('выполнена ежедневная рассылка')

            else:
                print(
                    "ничего не отправлено")  # Если ни одно из условий не выполнено, выводим сообщение о том, что ничего не отправлено.