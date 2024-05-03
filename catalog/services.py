from django.core.cache import cache

from catalog.models import Category
from config.settings import CACHE_ENABLED


def get_categories_from_cache():
    """Получает данные о категориях из кэша, если его нет, то из БД и запишет в кэш"""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'category_list'
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = Category.objects.all()
    cache.set(key, categories)
    return categories