from django.urls import path
from .views import BookListView, BookRetrieveUpdateDestroyAPIView, AveragePriceAPIView

app_name = 'books'

urlpatterns = [
    path('books/', BookListView.as_view(), name=BookListView.name),
    path('books/<str:id>/', BookRetrieveUpdateDestroyAPIView.as_view(), name=BookRetrieveUpdateDestroyAPIView.name),
    path('books/average-price/<int:year>/', AveragePriceAPIView.as_view(), name=AveragePriceAPIView.name),
]