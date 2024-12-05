from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("book/", include("book.urls", namespace="book")),
    path("borrowing/", include("borrowing.urls", namespace="borrowing")),
    path("user/", include("user.urls", namespace="user"))
]
