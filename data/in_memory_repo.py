from typing import List, Dict
from data.models import Book
from data.repository import BookRepository

class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.books: Dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        self.books[book.id] = book

    def get_all_books(self) -> List[Book]:
        return list(self.books.values())

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        return [
            book for book in self.books.values()
            if query in book.title.lower() or query in book.author.lower()
        ]

    def update_book(self, book: Book) -> None:
        if book.id in self.books:
            self.books[book.id] = book

    def delete_book(self, book_id: str) -> None:
        if book_id in self.books:
            del self.books[book_id]

    def update_quantity(self, book_id: str, quantity_change: int) -> None:
        if book_id in self.books:
            self.books[book_id].quantity += quantity_change
