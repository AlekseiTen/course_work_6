import random

from config.settings import CACHE_ENABLED
from django.core.cache import cache
from blog.models import Blog


def get_cached_articles():
    """функция для получения случайных статей из блога, и кэширования их"""

    # Если кэш выключен, получаем из бд
    # Получаем случайные 3 статьи (или меньше, если их меньше 3), иначе возв. пустой список
    if not CACHE_ENABLED:
        all_articles = Blog.objects.filter(is_published=True)
        if all_articles.exists():
            return random.sample(list(all_articles), min(3, all_articles.count()))
        else:
            return []

    key = "index_random_articles"  # Устанавливаем ключ для кэширования статей
    articles = cache.get(key)  # Пытаемся получить статьи из кэша по заданному ключу

    if articles is not None:
        return articles
    all_articles = Blog.objects.filter(is_published=True)
    if all_articles.exists():
        articles = random.sample(list(all_articles), min(3, all_articles.count()))
    else:
        articles = []
    cache.set(key, articles, 60)
    return articles
