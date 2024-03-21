from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('title',)


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    avatar = models.ImageField(upload_to='products/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('title',)
