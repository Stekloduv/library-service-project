from django.contrib import admin

from book.models import Book, Borrowing

admin.site.register(Book)
admin.site.register(Borrowing)
