
from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter

author_router = SimpleRouter()
book_router = SimpleRouter()
lib_router = SimpleRouter()
me_router = SimpleRouter()

author_router.register('books', views.AuthorBookViewset,
                       basename='author')
me_router.register('books', views.UserBookCopyViewset, basename='my books')
lib_router.register('copies', views.LibrarianBookViewset, basename='librian')
book_router.register('books', views.BookViewset, basename='books')

urlpatterns = [
    path("author/", include(author_router.urls)),
    path("", include(book_router.urls)),
    path("lib/", include(lib_router.urls)),
    path("me/", include(me_router.urls)),
]
"""
GET books/
GET books/<str:isbn>/

GET me/books?category=borrowed|reserved|requested
PUT me/books/<str:isbn>

GET author/books  
POST author/books
GET author/books/<str:isbn>
PUT author/books/<str:isbn>
DELETE author/books/<str:isbn>

GET lib/books?category=borrowed|reserved|requested
POST lib/copies
PUT lib/copies/<str:isbn>
"""

# urlpatterns = [
#     path('lib/add', views.add_copy, name='index'),
#     path('lib/copies', views.all_borrowed, name='index'),
#     path('lib/copies/<str:isbn>/update', views.change_copy, name='index'),
# ]
#
# urlpatterns += [
#     # path('me/return', views.index, name='index'),
#     path('me/reserve/<str:isbn>', views.reserve_book, name='index'),
#     path('me/books', views.get_my_books, name='index')
#     # path('me/borrowed', views.index, name='index'),
# ]
#
# urlpatterns += [
#     path('books/', views.get_all_books, name='get_all_books'),
#     path('books/<str:isbn>', views.get_detail_book, name='get_detail_book'),
# ]
#
# urlpatterns += [
#     path('accounts/login', views.login_view, name='login'),
#     path('accounts/logout', views.logout_view, name='logout'),
#     path('accounts/signup', views.signup_view, name='signup'),
# ]
#
# urlpatterns += [
#     path('author/publish', views.publish_book, name='index'),
#     path('author/books', views.my_publish, name='index'),
#     path('author/books/<str:isbn>/update', views.update_book, name='index'),
#     path('author/books/<str:isbn>/delete', views.delete_book, name='index'),
# ]
