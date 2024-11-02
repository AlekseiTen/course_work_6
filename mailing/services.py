import random

from config.settings import CACHE_ENABLED
from django.core.cache import cache
from blog.models import Blog


def get_cached_articles():
    """функция для получения случайных статей из блога, и кэширования их"""

    # Проверяем, включен ли кэш.
    if CACHE_ENABLED:
        key = 'index_random_articles'
        # Задаем ключ для кэша, который будет использоваться для хранения случайных статей.

        articles = cache.get(key)
        # Пытаемся получить статьи из кэша по заданному ключу.

        if articles is None:
            # Если статьи не найдены в кэше (articles равен None), выполняем следующий блок кода.

            articles = Blog.objects.filter(is_published=True)
            # Получаем все опубликованные статьи из модели Blog.

            if articles.exists():
                # Проверяем, существуют ли полученные статьи.

                articles = random.sample(list(articles), min(3, articles.count()))
                # Если статьи существуют, выбираем случайные 3 статьи (или меньше, если их меньше 3) из списка статей.

            cache.set(key, articles, 30)
            # Сохраняем выбранные статьи в кэш с заданным ключом на 10 секунд.

    else:
        # Если кэш не включен, выполняем следующий блок кода.

        articles = Blog.objects.filter(is_published=True)
        if articles.exists():
            articles = random.sample(list(articles), min(3, articles.count()))

    return articles
    # Возвращаем выбранные статьи (из кэша или из базы данных).
