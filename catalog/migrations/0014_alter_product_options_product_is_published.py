# Generated by Django 4.2.2 on 2024-04-25 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_product_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('title',), 'permissions': [('can_cancel_publication', 'Can cancel publication'), ('can_change_description', 'Can change description'), ('can_change_category', 'Can change category')], 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
    ]