from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from book.models import Book
from decimal import Decimal
from django.core.exceptions import ValidationError

from book.serializers import BookSerializer, BookListSerializer


class BookModelTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": Book.CoverType.HARD,
            "inventory": 10,
            "daily_fee": Decimal("5.00"),
        }

    def test_book_creation(self):
        book = Book.objects.create(**self.valid_data)
        self.assertEqual(book.title, self.valid_data["title"])
        self.assertEqual(book.author, self.valid_data["author"])
        self.assertEqual(book.cover, self.valid_data["cover"])
        self.assertEqual(book.inventory, self.valid_data["inventory"])
        self.assertEqual(book.daily_fee, self.valid_data["daily_fee"])

    def test_book_invalid_inventory(self):
        self.valid_data["inventory"] = 0
        book = Book(**self.valid_data)
        with self.assertRaises(ValidationError):
            book.full_clean()  # Triggers validation

    def test_book_invalid_daily_fee(self):
        self.valid_data["daily_fee"] = Decimal("0.00")
        book = Book(**self.valid_data)
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_str_representation(self):
        book = Book.objects.create(**self.valid_data)
        expected_str = f"{book.title} by {book.author} ({book.cover})"
        self.assertEqual(str(book), expected_str)


class BookSerializerTests(TestCase):
    def setUp(self):
        # Create a sample book
        self.book = Book.objects.create(
            title="Sample Book",
            author="Author Name",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=Decimal("5.00"),
        )

    def test_book_serializer(self):
        # Serialize the book
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Sample Book",
            "author": "Author Name",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "5.00",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_list_serializer(self):
        # Serialize the book using BookListSerializer
        serializer = BookListSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Sample Book",
            "author": "Author Name",
            "daily_fee": "5.00",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_detail_serializer(self):
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            "id": self.book.id,
            "title": "Sample Book",
            "author": "Author Name",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": "5.00",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_book_serializer_validation(self):
        valid_data = {
            "title": "New Book",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": "3.50",
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "New Book")

    def test_book_serializer_invalid_data(self):
        invalid_data = {
            "title": "",
            "author": "New Author",
            "cover": "SOFT",
            "inventory": 0,
            "daily_fee": "-5.00",
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("inventory", serializer.errors)
        self.assertIn("daily_fee", serializer.errors)


User = get_user_model()


class BookListViewTests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="password",
        )

        # Create some books
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=Decimal("5.00"),
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            cover=Book.CoverType.SOFT,
            inventory=5,
            daily_fee=Decimal("3.50"),
        )

        # Generate tokens
        self.user_token = AccessToken.for_user(self.user)
        self.admin_token = AccessToken.for_user(self.admin_user)

    def test_list_books_as_anonymous_user(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_books_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book_as_anonymous_user(self):
        response = self.client.get(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_retrieve_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_as_anonymous_user(self):
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "cover": Book.CoverType.HARD,
            "inventory": 15,
            "daily_fee": Decimal("6.00"),
        }
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "cover": Book.CoverType.HARD,
            "inventory": 15,
            "daily_fee": Decimal("6.00"),
        }
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_as_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "Book Three",
            "author": "Author Three",
            "cover": Book.CoverType.HARD,
            "inventory": 15,
            "daily_fee": Decimal("6.00"),
        }
        response = self.client.post("/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_update_book_as_anonymous_user(self):
        data = {"title": "Updated Book"}
        response = self.client.put(f"/books/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        data = {"title": "Updated Book"}
        response = self.client.put(f"/books/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "Updated Book",
            "author": self.book1.author,
            "cover": self.book1.cover,
            "inventory": self.book1.inventory,
            "daily_fee": self.book1.daily_fee,
        }
        response = self.client.put(f"/books/{self.book1.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])

    def test_delete_book_as_anonymous_user(self):
        response = self.client.delete(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_as_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.delete(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_as_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(f"/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
