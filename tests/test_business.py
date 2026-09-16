import pytest
import datetime
from data.models import Book
from data.in_memory_repo import InMemoryBookRepository
from business.book_manager import BookManager, ValidationError, CheckoutError, NotFoundError

@pytest.fixture
def manager():
    # Instantiate BookManager with the InMemory fake data source
    repo = InMemoryBookRepository()
    return BookManager(repo)

def test_add_valid_book(manager):
    book = Book(id="1", title="1984", author="George Orwell", isbn="1234567890", publication_year=1949, quantity=5)
    manager.add_book(book)
    books = manager.get_all_books()
    assert len(books) == 1
    assert books[0].title == "1984"

def test_add_book_empty_title(manager):
    book = Book(id="2", title="   ", author="Author", isbn="1234567890", publication_year=2000, quantity=1)
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        manager.add_book(book)

def test_add_book_invalid_isbn(manager):
    book = Book(id="3", title="Title", author="Author", isbn="123", publication_year=2000, quantity=1)
    with pytest.raises(ValidationError, match="ISBN must be exactly 10 or 13 digits"):
        manager.add_book(book)

def test_add_book_future_year(manager):
    future_year = datetime.date.today().year + 5
    book = Book(id="4", title="Title", author="Author", isbn="1234567890", publication_year=future_year, quantity=1)
    with pytest.raises(ValidationError, match="Publication year cannot be in the future"):
        manager.add_book(book)

def test_checkout_book_success(manager):
    book = Book(id="5", title="Title", author="Author", isbn="1234567890", publication_year=2000, quantity=2)
    manager.add_book(book)
    manager.checkout_book("5")
    updated_book = manager.get_all_books()[0]
    assert updated_book.quantity == 1

def test_checkout_book_zero_quantity(manager):
    book = Book(id="6", title="Title", author="Author", isbn="1234567890", publication_year=2000, quantity=0)
    manager.add_book(book)
    with pytest.raises(CheckoutError, match="Quantity is already 0"):
        manager.checkout_book("6")
