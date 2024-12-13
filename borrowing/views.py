from django.utils.timezone import now
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from borrowing.tasks import notify_overdue_borrowings
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer,
)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve"]:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        elif self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        if book.inventory <= 0:
            raise ValidationError({"error": "This book is out of stock."})

        book.inventory -= 1
        book.save()

        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = get_object_or_404(Borrowing, pk=pk)

        if borrowing.actual_return_date:
            return Response(
                {"error": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = now()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response(
            {"message": "Borrowing successfully returned."}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="notify-overdue")
    def notify_overdue(self, request):
        """
        Trigger the notification for overdue borrowings.
        """
        notify_overdue_borrowings.delay()  # Call the Celery task asynchronously
        return Response(
            {"message": "Notification for overdue borrowings has been triggered."},
            status=status.HTTP_200_OK,
        )

