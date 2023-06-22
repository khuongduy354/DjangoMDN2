from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import uuid


# class User(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     date_of_birth = models.DateField()
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
    due_date = models.DateField(null=True, default=None)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    AVAIL_CHOICES = (
        ('a', 'Available'),
        ('r', 'Reserved'),
        ('b', 'Borrowed')
    )

    availability = models.CharField(
        choices=AVAIL_CHOICES, default="a", max_length=1)

    requests = models.ManyToManyField(User, related_name="requests")

    class Meta:
        permissions = (
            ("can_see_all_borrowed", "can see all borrowed book copies"),
            ("can_see_my_borrowed", "can see my borrowed book copies"),
        )


# class BookBorrowCard(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     book = models.ForeignKey("BookCopy", on_delete=models.CASCADE)
#     borrower = models.ForeignKey(User, on_delete=models.CASCADE)


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
