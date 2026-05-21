from rest_framework import serializers
from .models import Loan
from books.serializers import BookListDetailSerializer


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('user', 'borrow_date', 'actual_return_date')


class LoanDetailSerializer(serializers.ModelSerializer):
    book = BookListDetailSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'
