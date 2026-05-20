from rest_framework import serializers
from .models import Book
from authors.serializers import AuthorSerializer


class BookSerializer(serializers.ModelSerializer):
    # Сериализатор для создания и обновления (принимает ID автора)
    class Meta:
        model = Book
        fields = '__all__'


class BookListDetailSerializer(serializers.ModelSerializer):
    # Сериализатор для красивого вывода (показывает данные автора внутри книги)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
