````markdown
# Flask CRUD API

A production-ready REST API built with Flask and SQLAlchemy for managing book records. Features comprehensive CRUD operations, input validation, error handling, and detailed API documentation.

## 🚀 Features

- **Full CRUD Operations**: Create, read, update, and delete book records
- **Comprehensive Validation**: Input validation with detailed error messages
- **Error Handling**: Global error handlers with consistent JSON responses
- **RESTful Design**: Standard HTTP methods and status codes
- **SQLAlchemy ORM**: Database abstraction with SQLite (PostgreSQL ready)
- **Pagination Support**: Query results with limit and offset parameters
- **Factory Pattern**: Clean application initialization with config support
- **Production Ready**: WSGI compatible, Gunicorn deployment ready
- **Well Documented**: Detailed docstrings and API documentation

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Error Handling](#error-handling)
- [Project Structure](#project-structure)
- [Technologies](#technologies)

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/Ameet225/flask-crud-api.git
cd flask-crud-api
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables**
```bash
cp .env.example .env
```

6. **Initialize the database**
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## ⚙️ Configuration

The application supports multiple environments: **development**, **testing**, and **production**.

### Environment Variables

Create a `.env` file in the project root:

```
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Configuration Details

- **FLASK_ENV**: Controls debug mode and reloader
  - `development`: Debug mode enabled, auto-reloader active
  - `production`: Debug mode disabled, no auto-reloader
  
- **FLASK_HOST**: Server listening address (default: 0.0.0.0)
- **FLASK_PORT**: Server listening port (default: 5000)
- **DATABASE_URL**: Database connection string (optional, defaults to SQLite)

## 🏃 Running the Application

### Development Mode

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Production Mode (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

## 📚 API Endpoints

Base URL: `http://localhost:5000/api`

### 1. Create a Book
**POST** `/books`

Create a new book record.

**Request:**
```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "year": 1925,
  "price": 12.99
}
```

**Response:** `201 Created`
```json
{
  "message": "Book created successfully",
  "data": {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1925,
    "price": 12.99,
    "created_at": "2024-07-20T10:30:00",
    "updated_at": "2024-07-20T10:30:00"
  }
}
```

### 2. Get All Books
**GET** `/books`

Retrieve all books with pagination support.

**Query Parameters:**
- `limit` (int): Maximum number of books to return (default: 100, max: 1000)
- `offset` (int): Number of books to skip (default: 0)

**Example:**
```bash
curl "http://localhost:5000/api/books?limit=10&offset=0"
```

**Response:** `200 OK`
```json
{
  "message": "Books retrieved successfully",
  "data": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "year": 1925,
      "price": 12.99,
      "created_at": "2024-07-20T10:30:00",
      "updated_at": "2024-07-20T10:30:00"
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 10,
    "offset": 0,
    "returned": 1
  }
}
```

### 3. Get a Specific Book
**GET** `/books/<id>`

Retrieve a single book by ID.

**Example:**
```bash
curl http://localhost:5000/api/books/1
```

**Response:** `200 OK`
```json
{
  "message": "Book retrieved successfully",
  "data": {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1925,
    "price": 12.99,
    "created_at": "2024-07-20T10:30:00",
    "updated_at": "2024-07-20T10:30:00"
  }
}
```

### 4. Update a Book
**PUT** `/books/<id>`

Update a book record (full or partial update).

**Request:**
```json
{
  "price": 14.99,
  "year": 1926
}
```

**Response:** `200 OK`
```json
{
  "message": "Book updated successfully",
  "data": {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1926,
    "price": 14.99,
    "created_at": "2024-07-20T10:30:00",
    "updated_at": "2024-07-20T10:35:00"
  }
}
```

### 5. Delete a Book
**DELETE** `/books/<id>`

Delete a book record.

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/books/1
```

**Response:** `200 OK`
```json
{
  "message": "Book with ID 1 deleted successfully",
  "deleted_id": 1
}
```

## 📤 Request/Response Examples

### Using cURL

**Create a book:**
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "price": 13.99
  }'
```

**Get all books:**
```bash
curl http://localhost:5000/api/books
```

**Get a specific book:**
```bash
curl http://localhost:5000/api/books/1
```

**Update a book:**
```bash
curl -X PUT http://localhost:5000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 15.99}'
```

**Delete a book:**
```bash
curl -X DELETE http://localhost:5000/api/books/1
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Create a book
response = requests.post(f"{BASE_URL}/books", json={
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937,
    "price": 11.99
})
print(response.json())

# Get all books
response = requests.get(f"{BASE_URL}/books")
print(response.json())

# Get a specific book
response = requests.get(f"{BASE_URL}/books/1")
print(response.json())

# Update a book
response = requests.put(f"{BASE_URL}/books/1", json={"price": 16.99})
print(response.json())

# Delete a book
response = requests.delete(f"{BASE_URL}/books/1")
print(response.json())
```

## ⚠️ Error Handling

The API returns consistent JSON error responses with appropriate HTTP status codes.

### Error Response Format

```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

### Common Errors

| Status | Error | Message |
|--------|-------|---------|
| 400 | Validation Error | Title cannot be empty |
| 400 | Invalid Content-Type | Request body must be JSON |
| 404 | Not Found | Book with ID 1 does not exist |
| 409 | Duplicate Record | Book with title 'Title' already exists |
| 405 | Method Not Allowed | HTTP method not supported |
| 500 | Internal Server Error | Database error occurred |

### Validation Rules

**Title:**
- Required for creation
- Must be a non-empty string
- Maximum 255 characters
- Must be unique

**Author:**
- Required for creation
- Must be a non-empty string
- Maximum 255 characters

**Year:**
- Required for creation
- Must be an integer between 1000 and current year + 1

**Price:**
- Required for creation
- Must be a positive number
- Maximum value: 999,999.99

## 📁 Project Structure

```
flask-crud-api/
├── app/
│   ├── __init__.py          # App factory and configuration
│   ├── models.py            # SQLAlchemy models (Book)
│   └── routes.py            # API endpoints and error handlers
├── instance/                # Instance-specific files
│   └── app.db               # SQLite database (auto-created)
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore patterns
└── README.md                # This file
```

### File Descriptions

- **app/__init__.py**: Application factory with Flask and SQLAlchemy setup
- **app/models.py**: SQLAlchemy ORM models for database tables
- **app/routes.py**: REST API endpoints and comprehensive error handling
- **run.py**: Entry point for running the application
- **requirements.txt**: All Python package dependencies
- **.env.example**: Template for environment configuration
- **.gitignore**: Git patterns for version control

## 🛠️ Technologies

- **Flask** (3.0.0): Web framework
- **Flask-SQLAlchemy** (3.1.1): ORM integration
- **SQLAlchemy** (2.0.23): Object-relational mapping
- **Gunicorn** (21.2.0): WSGI HTTP server
- **Python** (3.8+): Programming language

## 📝 Database Schema

### Book Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT |
| title | String(255) | NOT NULL, UNIQUE, INDEXED |
| author | String(255) | NOT NULL |
| year | Integer | NOT NULL |
| price | Float | NOT NULL |
| created_at | DateTime | NOT NULL, DEFAULT: NOW |
| updated_at | DateTime | NOT NULL, DEFAULT: NOW, ON UPDATE: NOW |

## 🚀 Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 run:app
```

### Environment Variables for Production

```
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/db_name
```

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Ameet Vikram**
- GitHub: [@Ameet225](https://github.com/Ameet225)

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Last Updated:** July 20, 2024
````
