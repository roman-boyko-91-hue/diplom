from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from authors.models import Author
from .models import Book


User = get_user_model()


class LibraryProjectTests(APITestCase):

    def setUp(self):
        # 1. Создаем тестовых пользователей
        self.librarian = User.objects.create_user(email="lib@test.com", password="password123", is_librarian=True)
        self.reader = User.objects.create_user(email="reader@test.com", password="password123", is_librarian=False)

        # 2. Создаем тестового автора и книгу
        self.author = Author.objects.create(first_name="Иван", last_name="Тургенев")
        self.book = Book.objects.create(
            title="Отцы и дети",
            author=self.author,
            isbn="1234567890",
            available_copies=1
        )

        # URL-адреса
        self.register_url = reverse('user-register')
        self.loan_url = reverse('book_loan')

    # USER & JWT TESTS
    def test_user_registration_and_password_is_write_only(self):
        """Тест регистрации и скрытия пароля (write_only)"""
        data = {"email": "newuser@test.com", "password": "securepwd125"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что в ответе НЕТ пароля (хеша)
        self.assertNotIn('password', response.data)

    # PERMISSIONS TESTS
    def test_reader_cannot_create_book(self):
        """Тест ограничений: читатель не может создавать книги"""
        self.client.force_authenticate(user=self.reader)
        url = reverse('book-list')
        data = {"title": "Новая книга", "isbn": "00000", "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_librarian_can_create_book(self):
        """Тест прав: библиотекарь может создавать книги"""
        self.client.force_authenticate(user=self.librarian)
        url = reverse('book-list')
        data = {"title": "Новая книга", "isbn": "999999", "author": self.author.id, "available_copies": 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ТЕСТ для книг
    def test_book_loan_and_return_toggle_logic(self):
        """Тест выдачи, уменьшения копий, возврата и их увеличения"""
        self.client.force_authenticate(user=self.reader)

        # 1. Берем книгу
        data = {"book": self.book.id}
        response = self.client.post(self.loan_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Книга взята')

        # Проверяем, что количество копий уменьшилось до 0
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 0)

        # 2: Возвращаем книгу (тот же запрос на тот же эндпоинт)
        response = self.client.post(self.loan_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Книга возвращена')

        # Проверяем, что количество копий вернулось к 1
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)

    def test_prohibition_of_loan_when_no_copies(self):
        """Тест запрета выдачи, если доступных копий 0"""
        self.book.available_copies = 0
        self.book.save()

        self.client.force_authenticate(user=self.reader)
        data = {"book": self.book.id}
        response = self.client.post(self.loan_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
