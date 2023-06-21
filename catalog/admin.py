from django.contrib import admin
from catalog.models import Author, Book, BookCopy, Genre
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Author)
admin.site.register(Genre)


# Register your models here.
