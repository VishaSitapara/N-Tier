from abc import ABC, abstractmethod
from typing import List
from data.models import Book

class BookRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> None:
        pass
        
    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass
        
    @abstractmethod
    def search_books(self, query: str) -> List[Book]:
        pass
        
    @abstractmethod
    def update_book(self, book: Book) -> None:
        pass
        
    @abstractmethod
    def delete_book(self, book_id: str) -> None:
        pass
        
    @abstractmethod
    def update_quantity(self, book_id: str, quantity_change: int) -> None:
        pass
