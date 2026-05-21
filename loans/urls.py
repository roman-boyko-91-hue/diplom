from django.urls import path

from .views import BookLoanAPIView

urlpatterns = [
    path('loan/', BookLoanAPIView.as_view(), name='book_loan'),
    ]
