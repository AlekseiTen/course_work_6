# Generated by Django 4.2.2 on 2024-10-30 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="Название")),
                ("body", models.TextField(verbose_name="Содержание")),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/preview",
                        verbose_name="Изображение превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Признак публикации"
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="slug"
                    ),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост в блоге",
                "verbose_name_plural": "Посты в блоге",
            },
        ),
    ]