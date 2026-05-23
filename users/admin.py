from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Поля, которые отображаются в списке пользователей
    list_display = ('id', 'email', 'is_librarian', 'is_staff', 'is_active')

    # Поиск по email
    search_fields = ('email',)

    # Сортировка списка пользователей по умолчанию
    ordering = ('email',)

    # Переопределяем отображение полей при редактировании юзера (убираем username)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_librarian', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля для формы создания нового пользователя через админку
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_librarian', 'is_staff', 'is_active'),
        }),
    )
