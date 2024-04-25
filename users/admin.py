from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение пользователей в админке"""
    list_display = ('id', 'email',)