from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from books.models import Book
from .models import Loan
from .serializers import LoanSerializer


class BookLoanAPIView(APIView):
    @swagger_auto_schema(request_body=LoanSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book')
        book_item = get_object_or_404(Book, id=book_id)

        subs_item = Loan.objects.filter(user=user, book=book_item)

        if subs_item.exists():
            loan = Loan.objects.get(user=user, book=book_item)
            loan.actual_return_date = timezone.now()
            loan.save()
            message = 'Книга возвращена'
        else:
            Loan.objects.create(user=user, book=book_item, expected_return_date=timezone.now() + timedelta(days=30))
            message = 'Книга взята'

        return Response({"message": message})
