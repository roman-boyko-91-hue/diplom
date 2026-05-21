from django.db import models
from django.conf import settings
from books.models import Book


class Loan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name="Читатель"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='loans',
        verbose_name="Книга"
    )
    borrow_date = models.DateField("Дата выдачи", auto_now_add=True)
    expected_return_date = models.DateField("Ожидаемая дата возврата")
    actual_return_date = models.DateField("Фактическая дата возврата", blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} взял {self.book.title}"
