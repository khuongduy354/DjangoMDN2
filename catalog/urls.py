
from django.urls import path
from . import views
urlpatterns = [
    path('lib/add', views.index, name='index'),
    path('lib/borrowed', views.index, name='index'),
    path('lib/change', views.index, name='index'),
]

urlpatterns += [
    path('me/return', views.index, name='index'),
    path('me/borrow', views.index, name='index'),
    path('me/borrowed', views.index, name='index'),
]

urlpatterns += [
    path('books/', views.get_all_books, name='get_all_books'),
    path('books/<str:isbn>', views.get_detail_book, name='get_detail_book'),
]

urlpatterns += [
    path('accounts/login', views.index, name='index'),
    path('accounts/logout', views.index, name='index'),
    path('accounts/signup', views.index, name='index'),
]

urlpatterns += [
    path('author/publish', views.index, name='index'),
    path('author/books/<int>/update', views.index, name='index'),
    path('author/books/<int>/delete', views.index, name='index'),
    path('author/books/<int>', views.index, name='index'),
]
