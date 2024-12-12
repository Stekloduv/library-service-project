from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils.timezone import now
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from book.models import Book
from user.models import User
from borrowing.models import Borrowing


class BorrowingModelTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )

        # Create a book with a valid daily price
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=Decimal("10.00"),
        )

    def test_calculate_total_price_valid(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 25),
            book=self.book,
            user=self.user,
        )
        total_fee = borrowing.calculate_total_fee()
        self.assertEqual(total_fee, Decimal("50.00"))

    def test_calculate_total_price_missing_daily_fee(self):
        self.book.daily_fee = None

        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 25),
            book=self.book,
            user=self.user,
        )

        with self.assertRaises(ValueError) as context:
            borrowing.calculate_total_fee()

        self.assertEqual(
            str(context.exception),
            f"The book '{self.book.title}' does not have a daily_fee.",
        )

    def test_calculate_total_fee_zero_days(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 20),
            book=self.book,
            user=self.user,
        )
        total_price = borrowing.calculate_total_fee()
        self.assertEqual(total_price, Decimal("0.00"))  # 0 days

    def test_calculate_total_fee_negative_days(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 25),
            expected_return_date=date(2024, 11, 20),  # Return date before borrow date
            book=self.book,
            user=self.user,
        )
        total_fee = borrowing.calculate_total_fee()
        self.assertEqual(total_fee, Decimal("-50.00"))  # -5 days * 10.00 daily price

    def test_str_representation(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date(2024, 11, 20),
            expected_return_date=date(2024, 11, 25),
            book=self.book,
            user=self.user,
        )
        self.assertEqual(
            str(borrowing), f"Borrowing: {self.book.title} by {self.user.username}"
        )


class BorrowingViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=Decimal("10.00"),
        )

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=now(),
            expected_return_date=now() + timedelta(days=7),
        )

        self.user_token = AccessToken.for_user(self.user)

    def test_list_borrowings(self):
        response = self.client.get("/borrowing/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_borrowing(self):
        response = self.client.get(f"/borrowing/{self.borrowing.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing.id)

    def test_list_borrowings_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(reverse("borrowing:borrowing-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_return_borrowing(self):
        response = self.client.post(f"/borrowing/{self.borrowing.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 6)

    def test_return_already_returned_borrowing(self):
        self.borrowing.actual_return_date = now()
        self.borrowing.save()

        response = self.client.post(f"/borrowing/{self.borrowing.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
