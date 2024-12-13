# Library Service Project

A Django-based web application for managing library borrowing, books, and users. The project supports integration with Stripe for payments, Telegram notifications, and has a robust test suite for reliable operations. The application is containerized using Docker for easy deployment.

## Features

		User Management: Supports user authentication and admin control.
		Book Inventory: Manage books, including titles, authors, pricing, and inventory.
		Borrowing System: Borrow books with expected return dates. Mark borrowed books as returned. Integration with Stripe for payment processing.
		API Documentation: Auto-generated API documentation using DRF Spectacular.
		Background Tasks: Celery tasks for async operations with Redis as the message broker.
		Test Suite: Comprehensive tests for models, views, and serializers.

## Tech Stack

		Backend: Django, Django REST Framework (DRF)
		Database: PostgreSQL
		Messaging: Redis, Celery
		Payments: Stripe
		Containerization: Docker & Docker Compose

## Installation

### 1. Clone the repository

```
git clone https://github.com/Stekloduv/library-service-project.git
```


### 2. Set up environment variables

Create a .env file in the root directory (env.sample to .env)

### 3. Build and run the Docker containers

Ensure Docker is installed and running, then execute:

```
docker-compose up --build
```

This will start:
	•	Web: Django app
	•	Database: PostgreSQL
	•	Message Broker: Redis

### 4. Apply migrations and create superuser

Open a terminal in the running container:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Access the application

	•	Visit: http://localhost:8000
	•	API Docs: http://localhost:8000/api/schema/swagger-ui/

## Testing

Run all tests with coverage:

```
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

## Usage

### 1. Add Books

Admins can add books to the inventory through the admin panel or API.

### 2. Borrow Books

	•	Users can borrow books and make payments through Stripe.
	•	Notifications are sent via Telegram.

### 3. Return Books

Mark borrowed books as returned to update inventory.

###  Endpoints:

	•	Books: /books/
	•	Borrowing: /borrowing/
	•	Payments: /payments/