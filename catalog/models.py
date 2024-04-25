from django.db import models

from users.models import User


class Category(models.Model):
    '''Модель категорий товара'''
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('title',)


class Product(models.Model):
    '''Модель товара'''
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    avatar = models.ImageField(upload_to='products/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('title',)
        permissions = [
            ('can_cancel_publication', "Can cancel publication"),
            ('can_change_description', "Can change description"),
            ('can_change_category', "Can change category")
        ]


class Version(models.Model):
    '''Модель версий товара'''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', null=True,
                                related_name='versions')
    number = models.CharField(max_length=10, verbose_name='номер версии')
    title = models.CharField(max_length=100, verbose_name='название')
    actual = models.BooleanField(default=False, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class Buyer(models.Model):
    '''Модель неавторизованного пользователя, задавшего вопрос в разделе "Контакты"'''
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'
        ordering = ('name',)


class Blog(models.Model):
    '''Модель блога в разделе новости'''
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug', null=True, blank=True)
    text = models.TextField(verbose_name='Содержимое')
    avatar = models.ImageField(upload_to='articles/', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ('title',)
