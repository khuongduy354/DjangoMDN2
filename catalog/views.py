from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from catalog.models import Book

# Create your views here.


def index(request):
    return JsonResponse({"message": "Hello, world!"})


def get_all_books(request):
    books = Book.objects.all()
    return JsonResponse(serializers.serialize("json", books), safe=False)


def get_detail_book(request, isbn):
    book = Book.objects.get(ISBN=isbn)
    return JsonResponse(serializers.serialize("json", [book]), safe=False)
