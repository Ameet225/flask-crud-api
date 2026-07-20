"""
Database models for the Flask CRUD API.

This module defines SQLAlchemy ORM models representing database tables.
Currently includes the Book model with full CRUD support.
"""

from app import db
from datetime import datetime


class Book(db.Model):
    """
    Book model representing a book record in the database.
    
    Attributes:
        id (int): Primary key, auto-incremented unique identifier
        title (str): Book title, required, unique constraint
        author (str): Author name, required
        year (int): Publication year, required
        price (float): Book price in USD, required, must be positive
        created_at (datetime): Timestamp when record was created
        updated_at (datetime): Timestamp when record was last updated
    
    Table name: book
    """
    
    __tablename__ = 'book'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Book attributes
    title = db.Column(db.String(255), nullable=False, unique=True, index=True)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Audit timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of Book instance."""
        return f'<Book id={self.id} title="{self.title}" author="{self.author}" year={self.year} price={self.price}>'
    
    def to_dict(self):
        """
        Convert Book instance to dictionary representation.
        
        Used for JSON serialization in API responses.
        
        Returns:
            dict: Dictionary containing book attributes and timestamps
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'price': self.price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """
        Create a Book instance from dictionary data.
        
        Used to populate model from request data. Does not persist to database.
        
        Args:
            data (dict): Dictionary containing book attributes
        
        Returns:
            Book: New Book instance with attributes set from data
        """
        book = Book()
        book.title = data.get('title')
        book.author = data.get('author')
        book.year = data.get('year')
        book.price = data.get('price')
        return book
