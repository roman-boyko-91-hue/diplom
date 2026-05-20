from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен для заполнения")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Удаляем стандартный username
    email = models.EmailField("Email адрес", unique=True)
    is_librarian = models.BooleanField("Является библиотекарем", default=False)

    USERNAME_FIELD = "email"  # Вход по Email
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
