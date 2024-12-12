from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from book.models import Book
from book.serializers import BookSerializer, BookListSerializer


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ["create", "update", "partial_update", "destroy"]:
            return request.user and request.user.is_staff
        return True


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action == "retrieve":
            return BookSerializer
        return BookSerializer
