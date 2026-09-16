import datetime
from typing import List
from data.models import Book
from data.repository import BookRepository

class ValidationError(Exception):
    """Raised when business rules validation fails."""
    pass

class CheckoutError(Exception):
    """Raised when a book cannot be checked out."""
    pass

class NotFoundError(Exception):
    """Raised when a requested book is not found."""
    pass

class BookManager:
    def __init__(self, repository: BookRepository):
        # Dependency Injection of the Data Tier
        self.repository = repository

    def _validate_book(self, book: Book) -> None:
        """Internal helper to enforce all business rules for a book."""
        if not book.title or not book.title.strip():
            raise ValidationError("Title cannot be empty.")
            
        if not book.author or not book.author.strip():
            raise ValidationError("Author cannot be empty.")
            
        current_year = datetime.date.today().year
        if book.publication_year > current_year:
            raise ValidationError(f"Publication year cannot be in the future (current year is {current_year}).")
            
        isbn_clean = str(book.isbn).replace("-", "").replace(" ", "")
        if not (len(isbn_clean) in (10, 13) and isbn_clean.isdigit()):
            raise ValidationError("ISBN must be exactly 10 or 13 digits.")
            
        if book.quantity < 0:
            raise ValidationError("Quantity cannot be negative.")

    def add_book(self, book: Book) -> None:
        self._validate_book(book)
        self.repository.add_book(book)

    def get_all_books(self) -> List[Book]:
        return self.repository.get_all_books()

    def search_books(self, query: str) -> List[Book]:
        if not query or not query.strip():
            return []
        return self.repository.search_books(query)

    def update_book(self, book: Book) -> None:
        self._validate_book(book)
        self.repository.update_book(book)

    def delete_book(self, book_id: str) -> None:
        if not book_id:
            raise ValidationError("Book ID must be provided.")
        self.repository.delete_book(book_id)
        
    def _get_book_by_id(self, book_id: str) -> Book:
        # Helper to find a book using the existing repository interface
        books = self.repository.get_all_books()
        for book in books:
            if str(book.id) == str(book_id):
                return book
        raise NotFoundError(f"Book with ID '{book_id}' not found.")

    def checkout_book(self, book_id: str) -> None:
        book = self._get_book_by_id(book_id)
        
        if book.quantity <= 0:
            raise CheckoutError(f"Cannot check out '{book.title}': Quantity is already 0.")
            
        self.repository.update_quantity(book_id, -1)
