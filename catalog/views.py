from django.core import serializers
from django.contrib.auth import logout, models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from catalog.models import Book, BookCopy

# Create your views here.


def index(request):
    return JsonResponse({"message": "Hello, world!"})


def get_all_books(request):
    books = Book.objects.all()
    return JsonResponse(serializers.serialize("json", books), safe=False)


def get_detail_book(request, isbn):
    book = Book.objects.get(ISBN=isbn)
    return JsonResponse(serializers.serialize("json", [book]), safe=False)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Successfully"})
        else:
            # error_message = 'Invalid username or password.'
            return HttpResponse(b"Invalid username or password.", status=401)
    else:
        return HttpResponse(b"Method not allowed", status=405)


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            error_message = b'Username already exists.'
            return HttpResponse(error_message, status=400)
        user = models.User.objects.create_user(
            username=username, password=password)
        return JsonResponse({"message": "Successfully"})
    else:
        return HttpResponse(b"Method not allowed", status=405)


def logout_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "Successfully"})
    else:
        return HttpResponse(b"Method not allowed or not Auth", status=405)


# personal
@permission_required('catalog.can_see_my_borrowed')
@login_required
def get_my_borrowed_books(request):
    if request.method == 'GET' and request.user.is_authenticated:
        books = BookCopy.objects.filter(borrower=request.user)
        return JsonResponse(serializers.serialize("json", books), safe=False)
    else:
        return HttpResponse(b"Method not allowed or not Auth", status=405)


@permission_required('catalog.can_see_my_borrowed')
@login_required
def borrow_book(request):
    if request.method == 'POST' and request.user.is_authenticated:
        book = BookCopy.objects.get(id=request.POST['book_id'])
        if book.available:
            book.borrower = request.user.id
            book.available = False
            book.save()
            return JsonResponse({"message": "Successfully"})
        else:
            return HttpResponse(b"Book is borrowed", status=400)
    else:
        return HttpResponse(b"Method not allowed or not Auth", status=405)


@permission_required('catalog.can_see_my_borrowed')
@login_required
def return_book(request):
    if request.method == 'POST' and request.user.is_authenticated:
        book = BookCopy.objects.get(id=request.POST['book_id'])
        if book.borrower != request.user.id:
            return HttpResponse(b"Book is not borrowed", status=400)
        else:
            book.borrower = None
            book.save()
            return JsonResponse({"message": "Successfully"})
    else:
        return HttpResponse(b"Method not allowed or not Auth", status=405)
