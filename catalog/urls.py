
from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter

author_router = SimpleRouter()
book_router = SimpleRouter()
lib_router = SimpleRouter()

author_router.register('books', views.AuthorBookViewset,
                       basename='author_books')
lib_router.register('copies', views.LibrarianBookViewset, basename='lib_books')
book_router.register('books', views.BookViewset, basename='books')

urlpatterns = [
    path("author/", include(author_router.urls)),
    path("", include(book_router.urls), name="books"),
    path("lib/", include(lib_router.urls), name="lib_book"),
    path("accounts/login", views.Login.as_view(), name="login"),
    path("accounts/logout", views.Logout.as_view(), name="logout"),
    path("accounts/signup", views.Signup.as_view(), name="signup"),
]


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
