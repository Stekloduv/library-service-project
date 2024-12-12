from decimal import Decimal

from django.db import models

from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(verbose_name="borrow_date")
    expected_return_date = models.DateField(verbose_name="expected_return_date")
    actual_return_date = models.DateField(
        verbose_name="Actual Return Date",
        null=True,
        blank=True,
        default=None,
    )
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")

    def calculate_total_fee(self) -> Decimal:
        duration = (self.expected_return_date - self.borrow_date).days
        daily_fee = getattr(self.book, "daily_fee", None)

        if daily_fee is None:
            raise ValueError(
                f"The book '{self.book.title}' does not have a daily_fee."
            )
        return Decimal(duration * daily_fee)

    def __str__(self) -> str:
        return f"Borrowing: {self.book.title} by {self.user.username}"

    @property
    def full_date(self):
        return f"{self.borrow_date} - {self.expected_return_date}"

    def __str__(self):
        return f"Borrowing: {self.book.title} by {self.user.username}"
