from rest_framework import serializers

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.PrimaryKeyRelatedField(
        queryset=Borrowing.objects.select_related("user", "book")
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentListSerializer(serializers.ModelSerializer):
    borrowing = serializers.CharField(source="borrowing.book.title", read_only=True)

    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing", "money_to_pay")


class PaymentRetrieveSerializer(PaymentSerializer):
    borrowing = BorrowingListSerializer(many=False, read_only=True)


class PaymentReadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "type", "money_to_pay")


class PaymentReadRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        )
