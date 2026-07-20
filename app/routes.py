"""
API routes and error handling for the Flask CRUD API.

This module defines all REST API endpoints for Book resource CRUD operations
and centralized error handling for the application. All responses are JSON.
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Book
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__)


# ============================================================================
# Validation Helper Functions
# ============================================================================

def validate_book_data(data, is_update=False):
    """
    Validate book data from request.
    
    Performs comprehensive validation of book attributes including type checking,
    range validation, and format validation.
    
    Args:
        data (dict): Dictionary containing book data to validate
        is_update (bool): If True, allows partial updates (not all fields required)
    
    Returns:
        tuple: (is_valid, error_message) where is_valid is bool and error_message is str or None
    """
    
    # Check for empty data
    if not data:
        return False, "Request body cannot be empty"
    
    # Determine required fields based on operation type
    required_fields = ['title', 'author', 'year', 'price'] if not is_update else []
    
    # Validate required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate title
    if 'title' in data:
        if data['title'] is None:
            return False, "Title cannot be null"
        if not isinstance(data['title'], str):
            return False, "Title must be a string"
        if len(data['title'].strip()) == 0:
            return False, "Title cannot be empty"
        if len(data['title']) > 255:
            return False, "Title must not exceed 255 characters"
    
    # Validate author
    if 'author' in data:
        if data['author'] is None:
            return False, "Author cannot be null"
        if not isinstance(data['author'], str):
            return False, "Author must be a string"
        if len(data['author'].strip()) == 0:
            return False, "Author cannot be empty"
        if len(data['author']) > 255:
            return False, "Author must not exceed 255 characters"
    
    # Validate year
    if 'year' in data:
        if data['year'] is None:
            return False, "Year cannot be null"
        if not isinstance(data['year'], int) or isinstance(data['year'], bool):
            return False, "Year must be an integer"
        if data['year'] < 1000 or data['year'] > datetime.utcnow().year + 1:
            return False, f"Year must be between 1000 and {datetime.utcnow().year + 1}"
    
    # Validate price
    if 'price' in data:
        if data['price'] is None:
            return False, "Price cannot be null"
        if not isinstance(data['price'], (int, float)) or isinstance(data['price'], bool):
            return False, "Price must be a number"
        if data['price'] < 0:
            return False, "Price cannot be negative"
        if data['price'] > 999999.99:
            return False, "Price exceeds maximum allowed value"
    
    # Check for unknown fields
    valid_fields = {'title', 'author', 'year', 'price'}
    for field in data.keys():
        if field not in valid_fields:
            return False, f"Unknown field: {field}"
    
    return True, None


# ============================================================================
# CRUD Endpoints
# ============================================================================

@api_bp.route('/books', methods=['POST'])
def create_book():
    """
    Create a new book record.
    
    Endpoint: POST /api/books
    
    Expected JSON:
        {
            "title": "Book Title",
            "author": "Author Name",
            "year": 2024,
            "price": 29.99
        }
    
    Returns:
        201: Created - Book successfully created with full book object
        400: Bad Request - Validation error or malformed JSON
        409: Conflict - Duplicate title already exists
        500: Server Error - Database error
    """
    
    # Check Content-Type
    if not request.is_json:
        return jsonify({
            'error': 'Invalid Content-Type',
            'message': 'Request body must be JSON (Content-Type: application/json)'
        }), 400
    
    # Parse JSON
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': 'Malformed JSON',
            'message': 'Request body contains invalid JSON'
        }), 400
    
    # Validate data
    is_valid, error_message = validate_book_data(data, is_update=False)
    if not is_valid:
        return jsonify({
            'error': 'Validation Error',
            'message': error_message
        }), 400
    
    # Create new book instance
    book = Book.from_dict(data)
    
    try:
        # Add to database
        db.session.add(book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book created successfully',
            'data': book.to_dict()
        }), 201
    
    except IntegrityError as e:
        db.session.rollback()
        
        # Check for duplicate title
        if 'UNIQUE constraint failed' in str(e) or 'unique' in str(e).lower():
            return jsonify({
                'error': 'Duplicate Record',
                'message': f"Book with title '{data['title']}' already exists"
            }), 409
        
        return jsonify({
            'error': 'Database Error',
            'message': 'Failed to create book due to integrity constraint'
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while creating the book'
        }), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': 'An unexpected error occurred'
        }), 500


@api_bp.route('/books', methods=['GET'])
def get_all_books():
    """
    Retrieve all books.
    
    Endpoint: GET /api/books
    
    Query Parameters:
        limit (int): Maximum number of books to return (default: 100, max: 1000)
        offset (int): Number of books to skip (default: 0)
    
    Returns:
        200: Success - List of all books with pagination metadata
        400: Bad Request - Invalid query parameters
        500: Server Error - Database error
    """
    
    try:
        # Get pagination parameters with validation
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        # Validate pagination parameters
        if limit < 1 or limit > 1000:
            return jsonify({
                'error': 'Invalid Parameter',
                'message': 'Limit must be between 1 and 1000'
            }), 400
        
        if offset < 0:
            return jsonify({
                'error': 'Invalid Parameter',
                'message': 'Offset must be non-negative'
            }), 400
        
        # Query books with pagination
        total_count = Book.query.count()
        books = Book.query.offset(offset).limit(limit).all()
        
        return jsonify({
            'message': 'Books retrieved successfully',
            'data': [book.to_dict() for book in books],
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'returned': len(books)
            }
        }), 200
    
    except ValueError as e:
        return jsonify({
            'error': 'Invalid Parameter',
            'message': 'Query parameters must be valid integers'
        }), 400
    
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while retrieving books'
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': 'An unexpected error occurred'
        }), 500


@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Retrieve a specific book by ID.
    
    Endpoint: GET /api/books/<id>
    
    Args:
        book_id (int): ID of the book to retrieve
    
    Returns:
        200: Success - Book object
        400: Bad Request - Invalid book ID
        404: Not Found - Book does not exist
        500: Server Error - Database error
    """
    
    # Validate book_id (already validated by route converter, but for safety)
    if not isinstance(book_id, int) or book_id < 1:
        return jsonify({
            'error': 'Invalid ID',
            'message': 'Book ID must be a positive integer'
        }), 400
    
    try:
        # Query for book
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({
                'error': 'Not Found',
                'message': f'Book with ID {book_id} does not exist'
            }), 404
        
        return jsonify({
            'message': 'Book retrieved successfully',
            'data': book.to_dict()
        }), 200
    
    except SQLAlchemyError as e:
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while retrieving the book'
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Server Error',
            'message': 'An unexpected error occurred'
        }), 500


@api_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Update a book by ID (full or partial update).
    
    Endpoint: PUT /api/books/<id>
    
    Args:
        book_id (int): ID of the book to update
    
    Expected JSON (partial update - any combination of fields):
        {
            "title": "Updated Title",
            "author": "Updated Author",
            "year": 2024,
            "price": 39.99
        }
    
    Returns:
        200: Success - Updated book object
        400: Bad Request - Validation error, malformed JSON, or invalid ID
        404: Not Found - Book does not exist
        409: Conflict - Duplicate title
        500: Server Error - Database error
    """
    
    # Validate book_id
    if not isinstance(book_id, int) or book_id < 1:
        return jsonify({
            'error': 'Invalid ID',
            'message': 'Book ID must be a positive integer'
        }), 400
    
    # Check Content-Type
    if not request.is_json:
        return jsonify({
            'error': 'Invalid Content-Type',
            'message': 'Request body must be JSON (Content-Type: application/json)'
        }), 400
    
    # Parse JSON
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': 'Malformed JSON',
            'message': 'Request body contains invalid JSON'
        }), 400
    
    # Validate data (allow partial updates)
    is_valid, error_message = validate_book_data(data, is_update=True)
    if not is_valid:
        return jsonify({
            'error': 'Validation Error',
            'message': error_message
        }), 400
    
    try:
        # Query for book
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({
                'error': 'Not Found',
                'message': f'Book with ID {book_id} does not exist'
            }), 404
        
        # Update book attributes
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'year' in data:
            book.year = data['year']
        if 'price' in data:
            book.price = data['price']
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'message': 'Book updated successfully',
            'data': book.to_dict()
        }), 200
    
    except IntegrityError as e:
        db.session.rollback()
        
        # Check for duplicate title
        if 'UNIQUE constraint failed' in str(e) or 'unique' in str(e).lower():
            return jsonify({
                'error': 'Duplicate Record',
                'message': f"Book with title '{data.get('title')}' already exists"
            }), 409
        
        return jsonify({
            'error': 'Database Error',
            'message': 'Failed to update book due to integrity constraint'
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while updating the book'
        }), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': 'An unexpected error occurred'
        }), 500


@api_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Delete a book by ID.
    
    Endpoint: DELETE /api/books/<id>
    
    Args:
        book_id (int): ID of the book to delete
    
    Returns:
        200: Success - Confirmation of deletion
        400: Bad Request - Invalid book ID
        404: Not Found - Book does not exist
        500: Server Error - Database error
    """
    
    # Validate book_id
    if not isinstance(book_id, int) or book_id < 1:
        return jsonify({
            'error': 'Invalid ID',
            'message': 'Book ID must be a positive integer'
        }), 400
    
    try:
        # Query for book
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({
                'error': 'Not Found',
                'message': f'Book with ID {book_id} does not exist'
            }), 404
        
        # Delete book
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({
            'message': f'Book with ID {book_id} deleted successfully',
            'deleted_id': book_id
        }), 200
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while deleting the book'
        }), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Server Error',
            'message': 'An unexpected error occurred'
        }), 500


# ============================================================================
# Health Check Endpoint
# ============================================================================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for application monitoring.
    
    Endpoint: GET /api/health
    
    Returns:
        200: Application is healthy
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ============================================================================
# Global Error Handlers
# ============================================================================

@api_bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors."""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource does not exist'
    }), 404


@api_bp.errorhandler(405)
def method_not_allowed_error(error):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({
        'error': 'Method Not Allowed',
        'message': 'The HTTP method used is not supported for this endpoint'
    }), 405


@api_bp.errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors."""
    return jsonify({
        'error': 'Bad Request',
        'message': 'The request is malformed or invalid'
    }), 400


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    db.session.rollback()
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred on the server'
    }), 500
