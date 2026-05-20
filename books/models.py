from django.db import models
from authors.models import Author


class Book(models.Model):
    title = models.CharField("Название книги", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор")
    genre = models.CharField("Жанр", max_length=100, blank=True, null=True)
    isbn = models.CharField("ISBN", max_length=20, unique=True)
    available_copies = models.PositiveIntegerField("Доступное количество копий", default=1)

    def __str__(self):
        return self.title
