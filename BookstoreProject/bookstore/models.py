from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000, message="Publication year must be at least 1000."),
            MaxValueValidator(2023, message="Publication year cannot exceed 2023."),
        ],
    )
    isbn = models.CharField(max_length=13)
    description = models.TextField()

    def __str__(self):
        return self.title






