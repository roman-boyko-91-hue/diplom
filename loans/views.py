from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from books.models import Book
from .models import Loan
from .serializers import LoanSerializer


class BookLoanAPIView(APIView):
    permission_classes = [IsAuthenticated] # Только для авторизованных пользователей по JWT!

    @swagger_auto_schema(request_body=LoanSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book')
        book_item = get_object_or_404(Book, id=book_id)

        # Ищем активный заем (где книга еще НЕ возвращена)
        subs_item = Loan.objects.filter(user=user, book=book_item, actual_return_date__isnull=True)

        if subs_item.exists():
            # ЛОГИКА ВОЗВРАТА
            loan = subs_item.first()
            loan.actual_return_date = timezone.now()
            loan.save()

            # УВЕЛИЧИВАЕМ количество доступных копий на 1
            book_item.available_copies += 1
            book_item.save()

            return Response({"message": 'Книга возвращена'}, status=status.HTTP_200_OK)
        else:
            # ЛОГИКА ВЫДАЧИ
            # ПРОВЕРКА: есть ли свободные экземпляры
            if book_item.available_copies <= 0:
                return Response(
                    {"error": "Нет доступных экземпляров данной книги в библиотеке"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Оформляем выдачу
            Loan.objects.create(
                user=user,
                book=book_item,
                expected_return_date=timezone.now() + timedelta(days=30)
            )

            # УМЕНЬШАЕМ количество доступных копий на 1
            book_item.available_copies -= 1
            book_item.save()

            return Response({"message": 'Книга взята'}, status=status.HTTP_201_CREATED)
