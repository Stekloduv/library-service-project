from django.db import models

from user.models import User


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
