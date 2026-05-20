from django.urls import path

from .views import UserCreateAPIView, UserDetailView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail')
]
