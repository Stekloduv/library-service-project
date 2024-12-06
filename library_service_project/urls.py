from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("book.urls", namespace="books")),
    path("borrowing/", include("borrowing.urls", namespace="borrowings")),
    path("user/", include("user.urls", namespace="user")),
]
