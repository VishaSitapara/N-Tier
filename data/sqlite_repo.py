import sqlite3
from typing import List
from data.models import Book
from data.repository import BookRepository

class SQLiteBookRepository(BookRepository):
    def __init__(self, db_path: str = "library.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL,
                    publication_year INTEGER NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')
            conn.commit()

    def _row_to_book(self, row) -> Book:
        return Book(
            id=row[0],
            title=row[1],
            author=row[2],
            isbn=row[3],
            publication_year=row[4],
            quantity=row[5]
        )

    def add_book(self, book: Book) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (id, title, author, isbn, publication_year, quantity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (book.id, book.title, book.author, book.isbn, book.publication_year, book.quantity))
            conn.commit()

    def get_all_books(self) -> List[Book]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, author, isbn, publication_year, quantity FROM books')
            rows = cursor.fetchall()
            return [self._row_to_book(row) for row in rows]

    def search_books(self, query: str) -> List[Book]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT id, title, author, isbn, publication_year, quantity 
                FROM books
                WHERE title LIKE ? OR author LIKE ?
            ''', (search_pattern, search_pattern))
            rows = cursor.fetchall()
            return [self._row_to_book(row) for row in rows]

    def update_book(self, book: Book) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE books
                SET title = ?, author = ?, isbn = ?, publication_year = ?, quantity = ?
                WHERE id = ?
            ''', (book.title, book.author, book.isbn, book.publication_year, book.quantity, book.id))
            conn.commit()

    def delete_book(self, book_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()

    def update_quantity(self, book_id: str, quantity_change: int) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE books
                SET quantity = quantity + ?
                WHERE id = ?
            ''', (quantity_change, book_id))
            conn.commit()
