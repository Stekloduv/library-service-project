"# library-service-project" 


Requirements:
Functional (what the system should do):
Web-based
Manage books inventory
Manage books borrowing
Manage customers
Display notifications
Handle payments
Non-functional (what the system should deal with):
5 concurrent users
Up to 1000 books
50k borrowings/year
~30MB/year


Resources:
Book:
Title: str
Author: str
Cover: Enum: HARD | SOFT
Inventory*: positive int
Daily fee: decimal (in $USD)

     * Inventory - the number of this specific book available for now in the library

User (Customer):
Email: str
First name: str
Last name: str
Password: str
Is staff: bool
Borrowing:
Borrow date: date
Expected return date: date
Actual return date: date
Book id: int
User id: int
Payment:
Status: Enum: PENDING | PAID
Type: Enum: PAYMENT | FINE
Borrowing id: int
Session url: Url  # url to stripe payment session
Session id: str  # id of stripe payment session
Money to pay: decimal (in $USD)  # calculated borrowing total price


.venv\scripts\activate