from users.permissions import IsLibrarianOrReadOnly
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer, BookListDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    # Подключаем фильтрацию и поиск
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genre']  # Фильтр по точному совпадению жанра
    search_fields = ['title', 'author__last_name', 'author__first_name']  # Поиск по названию и автору
    permission_classes = [IsLibrarianOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookListDetailSerializer
        return BookSerializer
