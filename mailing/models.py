from django.db import models

NULLABLE = {'blank': True, 'null': False}


class Client(models.Model):
    full_name = models.CharField(verbose_name="Ф.И.О клиента", max_length=255)
    email = models.EmailField(verbose_name="e-mail адрес", unique=True)
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема сообщения")
    body = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Активна"),
        ("completed", "Завершена"),
    ]

    PERIODICITY_CHOICES = [
        ("daily", "Ежедневно"),
        ("weekly", "Еженедельно"),
        ("monthly", "Ежемесячно"),
    ]

    description = models.CharField(
        verbose_name="описание", max_length=255, **NULLABLE
    )
    start_time = models.DateTimeField(auto_now=True, verbose_name="дата начала рассылки")
    periodicity = models.CharField(
        verbose_name="периодичность", max_length=10, choices=PERIODICITY_CHOICES
    )
    status = models.CharField(
        verbose_name="статус", max_length=10, choices=STATUS_CHOICES, default="created"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="сообщение"
    )
    clients = models.ManyToManyField(Client, verbose_name="клиенты")
    actual_end_time = models.DateTimeField(
        verbose_name="дата завершения рассылки", blank=True, null=True
    )

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingAttempt(models.Model):
    STATUS_CHOICES = [("success", "Успешно"), ("failed", "Не успешно")]

    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name='Рассылка'
    )
    send_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)

    def __str__(self):
        return f"Попытка {self.id} для рассылки {self.mailing.id}"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
