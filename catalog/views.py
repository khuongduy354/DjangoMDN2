from django.core import serializers
from django.contrib.auth import logout, models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import viewsets

from catalog.models import Book, BookCopy
from rest_framework import generics
from catalog.permission import AuthorPerm, LibrarianPerm, UserPerm

from catalog.serializer import BookCopySerializer, BookSerializer


def index(request):
    return JsonResponse({"message": "Hello, world!"})

# general


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "isbn"


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


@permission_classes([IsAuthenticated])
class Logout(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Successfully"})
        else:
            return Response(b"Method not allowed or not Auth", status=405)


# personal
@permission_classes([IsAuthenticated, UserPerm])
class UserBookCopyViewset(viewsets.ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
    lookup_field = 'isbn'

    """Show books depend on category"""

    def list(self, request):
        queryset = self.get_queryset()

        cat = request.query_params.get('category')
        if cat == "requested":
            queryset = BookCopy.objects.filter(requests=request.user.id)
        if cat == "reserved":
            books = BookCopy.objects.filter(
                borrower=request.user.id, availability="r")
        else:
            queryset = BookCopy.objects.filter(
                borrower=request.user.id, availability="b")

        serializer = BookCopySerializer(queryset, many=True)
        return Response(serializer.data)

    """Reserve book copies"""

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.availability == "a":
            queryset.requests.add(request.user.id)
            queryset.save()
            return Response({"message": "Successfully"})
        else:
            return Response(b"Book is borrowed", status=400)

# author


@permission_classes([IsAuthenticated, AuthorPerm])
class AuthorBookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn'  # use for delete, retrieve , update

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user.id)


# librarians
@permission_classes([IsAuthenticated, LibrarianPerm])
class LibrarianBookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn'

    def list(self):
        books = self.get_queryset()
        cat = self.request.query_params.get('category')
        if cat == "reserve":
            books = BookCopy.objects.filter(availability="r")
        if cat == "borrow":
            books = BookCopy.objects.filter(availability="b")
        else:
            books = BookCopy.objects.filter(requests__isnull=False)
        return Response(books)


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

# @permission_classes([IsAuthenticated, LibrarianPerm])
# class ChangeCopy(viewsets.ModelViewSet):
#     queryset = BookCopy.objects.all()
#     serializer_class = BookCopySerializer
#
#     def get_queryset(self):
#         return BookCopy.objects.get(isbn=self.kwargs['isbn'])
