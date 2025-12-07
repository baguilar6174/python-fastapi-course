# FastAPI Learning Project

A comprehensive learning project to understand FastAPI fundamentals including REST API development, database integration with SQLModel, authentication, testing, and subscription management.

## Features

- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Database Integration**: SQLite with SQLModel ORM for type-safe operations
- **Authentication**: HTTP Basic Auth implementation
- **Testing**: Comprehensive test suite with pytest and TestClient
- **Middleware**: Request timing and logging
- **Subscription System**: Customer-Plan relationships with status management
- **Email Validation**: Pydantic EmailStr with uniqueness constraints
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Getting Started

### Prerequisites
- Python 3.12+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
fastapi dev app/main.py
```

The API will be available at `http://localhost:8000` with automatic documentation at `http://localhost:8000/docs`

## Useful Commands

```bash
# Get library information like version
pip freeze | grep <library-name>
```

```bash
# create a simple seed (Customer and transactions)
python create_seed.py
```

```bash
# run tests (use -v flag for verbose output)
pytest
# run tests for specific file
pytest file-name -v
```

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app with auth, middleware, and routes
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── customers.py        # Customer CRUD operations
│   │   ├── transactions.py     # Transaction management
│   │   ├── invoices.py         # Invoice handling
│   │   └── plans.py            # Subscription plans
│   └── tests/
│       ├── __init__.py
│       ├── test_customers.py   # Customer endpoint tests
│       └── test.py
├── conftest.py                 # Pytest configuration and fixtures
├── models.py                   # SQLModel data models and relationships
├── db.py                       # Database configuration and session management
├── create_seed.py              # Database seeding script
├── requirements.txt            # Project dependencies
├── CLAUDE.md                   # AI assistant guidance
└── README.md                   # Project documentation
```

## API Endpoints

### Public Endpoints
- `GET /` - Hello World
- `GET /time/{iso_code}` - Get time by timezone

### Admin Endpoints (Basic Auth Required)
- `GET /admin` - Admin dashboard (username: admin, password: password)

### Customer Management
- `POST /customers` - Create customer
- `GET /customers` - List all customers
- `GET /customer/{id}` - Get customer by ID
- `PATCH /customer/{id}` - Update customer
- `DELETE /customer/{id}` - Delete customer
- `POST /customers/{customer_id}/plans/{plan_id}` - Subscribe customer to plan
- `GET /customers/{customer_id}/plans` - Get customer subscriptions

### Plans
- `POST /plans` - Create plan
- `GET /plans` - List plans

### Transactions
- `POST /transactions` - Create transaction
- `GET /transactions` - List transactions with pagination

### Invoices
- `POST /invoices` - Create invoice
- `GET /invoices` - List invoices

## Data Models

### Customer
- `name`: Customer name
- `email`: Unique email address (validated)
- `age`: Customer age
- `description`: Optional description

### Plan
- Subscription plans for customers
- Many-to-many relationship with customers via CustomerPlan

### Transaction
- `amount`: Transaction amount
- `description`: Transaction description
- Linked to customers via foreign key

### CustomerPlan
- Link table for customer-plan relationships
- `status`: ACTIVE/INACTIVE enum

## Learning Objectives

This project demonstrates key FastAPI concepts:

1. **Project Structure**: Organized router-based architecture
2. **Database Integration**: SQLModel for type-safe ORM operations
3. **Dependency Injection**: Session management and authentication
4. **Request Validation**: Pydantic models for input validation
5. **Error Handling**: Proper HTTP status codes and error responses
6. **Authentication**: HTTP Basic Auth implementation
7. **Middleware**: Request timing and logging
8. **Testing**: pytest with TestClient for API testing
9. **Documentation**: Automatic OpenAPI/Swagger generation
10. **Relationships**: One-to-many and many-to-many database relationships

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLModel**: Type-safe SQL database interactions (by same creator as FastAPI)
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for development
- **pytest**: Testing framework
- **httpx**: HTTP client for testing

## Stay in touch

- Website - [www.bryan-aguilar.com](https://www.bryan-aguilar.com/)
- Medium - [baguilar6174](https://baguilar6174.medium.com/)
- LinkedIn - [baguilar6174](https://www.linkedin.com/in/baguilar6174)