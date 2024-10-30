from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    body = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(upload_to="blog/preview", verbose_name="Изображение превью", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name="Признак публикации")
    slug = models.CharField(max_length=150, verbose_name="slug", **NULLABLE)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост в блоге'
        verbose_name_plural = 'Посты в блоге'
