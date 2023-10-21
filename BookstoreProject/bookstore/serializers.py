from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title','author','publication_year']

class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('image',)
