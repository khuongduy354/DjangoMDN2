from rest_framework.permissions import BasePermission


class LibrarianPerm(BasePermission):
    def has_permission(self, request, view):
        # Check if the requesting user has the custom permission
        return request.user.has_perm('catalog.can_see_all_borrowed')


class AuthorPerm(BasePermission):
    def has_permission(self, request, view):
        # Check if the requesting user has the custom permission
        return request.user.has_perm('catalog.can_add_book')


class UserPerm(BasePermission):
    def has_permission(self, request, view):
        # Check if the requesting user has the custom permission
        return request.user.has_perm('catalog.can_see_my_borrowed')
