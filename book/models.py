from django.db import models

from user.models import User


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverType.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrowing(models.Model):
    borrow_date = models.DateField(verbose_name="Borrow Date")
    expected_return_date = models.DateField(verbose_name="Expected Return Date")
    actual_return_date = models.DateField(
        verbose_name="Actual Return Date", null=True, blank=True
    )
    book = models.ForeignKey("Book", on_delete=models.CASCADE, verbose_name="Book ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User ID")

    def __str__(self):
        return f"Borrowing: {self.book.title} by {self.user.username}"
