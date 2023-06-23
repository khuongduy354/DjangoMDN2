from django.core import serializers
from django.contrib.auth import logout, models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from catalog.models import Book, BookCopy
from rest_framework import generics

from catalog.serializer import BookCopySerializer, BookSerializer


def index(request):
    return JsonResponse({"message": "Hello, world!"})

# General APIS


# def get_all_books(request):
#     books = Book.objects.all()
#     return JsonResponse(serializers.serialize("json", books), safe=False)
#

class ListBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class DetailBook(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"


# def get_detail_book(request, isbn):
#     book = Book.objects.get(ISBN=isbn)
#     return JsonResponse(serializers.serialize("json", [book]), safe=False)

class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Successfully"}, status=200)
        else:
            # error_message = 'Invalid username or password.'
            return Response(b"Invalid username or password.", status=401)


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({"message": "Successfully"})
#         else:
#             # error_message = 'Invalid username or password.'
#             return HttpResponse(b"Invalid username or password.", status=401)
#     else:
#         return HttpResponse(b"Method not allowed", status=405)
#
class Signup(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            error_message = b'Username already exists.'
            return Response(error_message, status=400)
        user = models.User.objects.create_user(
            username=username, password=password)
        return Response({"message": "Successfully"}, status=200)


# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             error_message = b'Username already exists.'
#             return HttpResponse(error_message, status=400)
#         user = models.User.objects.create_user(
#             username=username, password=password)
#         return JsonResponse({"message": "Successfully"})
#     else:
#         return HttpResponse(b"Method not allowed", status=405)

@permission_classes([IsAuthenticated])
class Logout(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Successfully"})
        else:
            return Response(b"Method not allowed or not Auth", status=405)

# def logout_view(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         logout(request)
#         return JsonResponse({"message": "Successfully"})
#     else:
        # return HttpResponse(b"Method not allowed or not Auth", status=405)


# personal
@permission_classes([IsAuthenticated])
class MyBooks(APIView):
    def get(self, request):
        # get borrowed books as default
        books = BookCopy.objects.filter(
            borrower=request.user.id, availability="b")
        cat = request.query_params.get('category')
        if cat == "requested":
            books = BookCopy.objects.filter(requests=request.user.id)
        if cat == "reserved":
            books = BookCopy.objects.filter(
                borrower=request.user.id, availability="r")

        return JsonResponse(serializers.serialize("json", books), safe=False)


# @permission_required('catalog.can_see_my_borrowed')
# @login_required
# def get_my_books(request):
#     if request.method == 'GET' and request.user.is_authenticated:
#         # get borrowed books as default
#         books = BookCopy.objects.filter(borrower=request.user.id)
#         cat = request.query_params.get('category')
#         if cat == "requested":
#             books = BookCopy.objects.filter(requests=request.user.id)
#         if cat == "reserved":
#             books = BookCopy.objects.filter(borrower=request.user.id)
#
#         return JsonResponse(serializers.serialize("json", books), safe=False)
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)

@permission_classes([IsAuthenticated])
class ReserveBook(APIView):
    def post(self, request, isbn):
        book = BookCopy.objects.get(isbn=isbn)
        if book.availability == "a":
            book.requests.add(request.user.id)
            book.save()
            return Response({"message": "Successfully"})
        else:
            return Response(b"Book is borrowed", status=400)

#
# @permission_required('catalog.can_see_my_borrowed')
# @login_required
# def reserve_book(request, isbn):
#     if request.method == 'POST' and request.user.is_authenticated:
#         book = BookCopy.objects.get(isbn=isbn)
#         if book.availability == "a":
#             book.requests.add(request.user.id)
#             book.save()
#             return JsonResponse({"message": "Successfully"})
#         else:
#             return HttpResponse(b"Book is borrowed", status=400)
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)


# @permission_required('catalog.can_see_my_borrowed')
# @login_required
# def return_book(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         book = BookCopy.objects.get(id=request.POST['book_id'])
#         if book.borrower != request.user.id:
#             return HttpResponse(b"Book is not borrowed", status=400)
#         else:
#             book.borrower = None
#             book.save()
#             return JsonResponse({"message": "Successfully"})
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)
#

# author
@permission_classes([IsAuthenticated])
class PublishBook(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# @ permission_classes([IsAuthenticated])
# class PublishBook(APIView):
#     def post(self, request):
#         if request.method == 'POST' and request.user.is_authenticated:
#             book = Book.objects.create(
#                 title=request.POST['title'],
#                 author=request.POST['author'],
#                 ISBN=request.POST['ISBN'],
#                 summary=request.POST['summary'],
#                 genre=request.POST['genre'],
#             )
#             book.save()
#             return Response({"message": "Successfully"})
# @login_required
# @permission_required('catalog.can_add_book')
# def publish_book(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         book = Book.objects.create(
#             title=request.POST['title'],
#             author=request.POST['author'],
#             ISBN=request.POST['ISBN'],
#             summary=request.POST['summary'],
#             genre=request.POST['genre'],
#         )
#         book.save()
#         return JsonResponse({"message": "Successfully"})

@permission_classes([IsAuthenticated])
class MyPublish(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user.id)


# @permission_required('catalog.can_add_book')
# @login_required
# def my_publish(request):
#     if request.method == 'GET' and request.user.is_authenticated:
#         books = Book.objects.filter(author=request.user.id)
#         return JsonResponse(serializers.serialize("json", books), safe=False)
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)
@permission_classes([IsAuthenticated])
class UpdateBook(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user.id, isbn=self.kwargs['isbn'])


# @permission_required('catalog.can_add_book')
# @login_required
# def update_book(request, isbn):
#     if request.method == 'PUT' and request.user.is_authenticated:
#         book = Book.objects.get(isbn=isbn)
#         book.title = request.POST['title']
#         book.author = request.POST['author']
#         book.ISBN = request.POST['ISBN']
#         book.summary = request.POST['summary']
#         book.genre = request.POST['genre']
#         book.save()
#         return JsonResponse({"message": "Successfully"})
#         return HttpResponse(b"Method not allowed or not Auth", status=405)
#     else:


@permission_classes([IsAuthenticated])
class DeleteBook(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.get(isbn=self.kwargs['isbn'], author=self.request.user.id)

#
# @permission_required('catalog.can_add_book')
# @login_required
# def delete_book(request, isbn):
#     if request.method == 'DELETE' and request.user.is_authenticated:
#         book = Book.objects.get(isbn=isbn)
#         if book.author != request.user.id:
#             return HttpResponse(b"Not author of this book", status=405)
#         book.delete()
#         return JsonResponse({"message": "Successfully"})
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)


# librarians
@permission_classes([IsAuthenticated])
class AddCopy(ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer

    def create(self):
        book = Book.objects.get(isbn=self.request.POST['isbn'])
        book_copy = BookCopy.objects.create(
            book=book,
        )
        book_copy.save()
        return Response({"message": "Successfully"})


# @permission_required('catalog.can_see_all_borrowed')
# @login_required
# def add_copy(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         book = Book.objects.get(isbn=request.POST['isbn'])
#         book_copy = BookCopy.objects.create(
#             book=book,
#         )
#         book_copy.save()
#         return JsonResponse({"message": "Successfully"})
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)
@permission_classes([IsAuthenticated])
class AllBorrowed(ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer

    def get_queryset(self):
        cat = self.request.query_params.get('category')
        # default to get requests books
        books = BookCopy.objects.filter(requests__isnull=False)
        if cat == "reserve":
            books = BookCopy.objects.filter(availability="r")
        if cat == "borrow":
            books = BookCopy.objects.filter(availability="b")
        return books


# @permission_required('catalog.can_see_all_borrowed')
# @login_required
# def all_borrowed(request):
#     if request.method == 'GET' and request.user.is_authenticated:
#         cat = request.query_params.get('category')
#         # default to get requests books
#         books = BookCopy.objects.filter(requests__isnull=False)
#         if cat == "reserve":
#             books = BookCopy.objects.filter(availability="r")
#         if cat == "borrow":
#             books = BookCopy.objects.filter(availability="b")
#         return JsonResponse(serializers.serialize("json", books), safe=False)
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)
#

@permission_classes([IsAuthenticated])
class ChangeCopy(ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer

    def get_queryset(self):
        return BookCopy.objects.get(isbn=self.kwargs['isbn'])

# @permission_required('catalog.can_see_all_borrowed')
# @login_required
# def change_copy(request, isbn):
#     if request.method == 'POST' and request.user.is_authenticated:
#         book = BookCopy.objects.get(isbn=isbn)
#         book.available = request.POST['available']
#         book.due_date = request.POST['due_back']
#         book.borrower = request.POST['borrower']
#
#         book.save()
#         return JsonResponse({"message": "Successfully"})
#     else:
#         return HttpResponse(b"Method not allowed or not Auth", status=405)
