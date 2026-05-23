from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в таблице всех выдач
    list_display = ('id', 'user', 'book', 'borrow_date', 'expected_return_date', 'actual_return_date')

    # Фильтры
    list_filter = ('borrow_date', 'actual_return_date')

    # Поиск по email читателя и названию книги
    search_fields = ('user__email', 'book__title')
