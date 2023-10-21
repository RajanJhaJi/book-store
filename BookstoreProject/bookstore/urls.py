from django.urls import path, include
from .views import get_books, add_book, list_books
urlpatterns = [
    path("books/",get_books),
    path("books/add",add_book),
    path("books/createlist",list_books)
]