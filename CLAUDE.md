# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI learning project that implements a REST API for managing customers, transactions, invoices, and plans using SQLite database with SQLModel ORM. The project includes subscription management where customers can subscribe to plans with different statuses.

## Common Commands

```bash
# Run the development server
fastapi dev app/main.py

# Install dependencies
pip install -r requirements.txt

# Check library versions
pip freeze | grep <library-name>
```

## Architecture

### Core Structure
- **app/main.py**: Main FastAPI application entry point with lifespan management, HTTP Basic Auth for admin endpoint, and request timing middleware
- **models.py**: SQLModel data models defining Customer, Transaction, Invoice, Plan, and CustomerPlan entities with relationships and email validation
- **db.py**: Database configuration with SQLite engine, session management, and dependency injection
- **app/routers/**: API route modules organized by domain (customers, transactions, invoices, plans)
- **app/tests/**: Test files using pytest with proper test client setup
- **conftest.py**: Pytest configuration with test database setup and FastAPI TestClient fixtures
- **create_seed.py**: Database seeding script for development data

### Database Design
- Uses SQLModel (Pydantic + SQLAlchemy) for type-safe database operations
- SQLite database (`db.sqlite3`) with automatic table creation on startup
- Customer-Transaction one-to-many relationship via foreign key
- Customer-Plan many-to-many relationship via CustomerPlan link table with status tracking
- Email validation with uniqueness constraints for customers
- Session dependency injection pattern (`SessionDependency`) for database operations

### Key Patterns
- Router-based organization with APIRouter instances included in main app
- Separate Create/Update/Base model classes for request validation
- Database session management through dependency injection
- Standard CRUD operations with proper HTTP status codes and error handling
- HTTP Basic Authentication for protected endpoints
- Request timing middleware for performance monitoring
- Test-driven development with pytest and TestClient
- Database seeding for development and testing

### Dependencies
- FastAPI with standard extras for web framework
- SQLModel for database ORM and validation
- Pydantic for data validation and serialization
- pytest for testing framework
- httpx for HTTP client testing (required for TestClient)
- SQLAlchemy for database operations