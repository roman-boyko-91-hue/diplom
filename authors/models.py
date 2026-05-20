from django.db import models


class Author(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    bio = models.TextField("Биография", blank=True, null=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
