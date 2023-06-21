from django.db import models
from django.db.models.fields import uuid


class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date_of_birth = models.DateField()
    # books = models.('Book')


class Book(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(max_length=1000)
    ISBN = models.CharField(max_length=255, primary_key=True, unique=True)
    # lang = models.ForeignKey('Language', on_delete=models.CASCADE)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # objects = models.Manager()
    genre = models.ManyToManyField('Genre')
    # objects = models.Manager()


class BookCopy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    available = models.BooleanField()
    due_date = models.DateField()


class BookBorrowCard(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    book = models.ForeignKey("BookCopy", on_delete=models.CASCADE)
    borrower = models.ForeignKey("User", on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date_of_birth = models.DateField()
    # books = models.('Book')


class Genre(models.Model):
    name = models.CharField(max_length=255)


# class Language(models.Model):
#     name = models.CharField(max_length=255)

# Create your models here.
