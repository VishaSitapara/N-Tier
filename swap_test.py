import os
from data.models import Book
from data.in_memory_repo import InMemoryBookRepository
from data.sqlite_repo import SQLiteBookRepository
from business.book_manager import BookManager

def run_business_logic(manager: BookManager, db_type: str):
    print(f"--- Running operations on {db_type} ---")
    
    # 1. Add a book
    book = Book(id="1", title="The Great Gatsby", author="F. Scott Fitzgerald", 
                isbn="1234567890", publication_year=1925, quantity=2)
    manager.add_book(book)
    print(f"Added book: {book.title}")
    
    # 2. View all books
    books = manager.get_all_books()
    print(f"Total books found: {len(books)}")
    
    # 3. Check out the book
    manager.checkout_book("1")
    updated_books = manager.get_all_books()
    print(f"Quantity after checkout: {updated_books[0].quantity}")
    print()

def main():
    # Use a temporary sqlite DB file for the test
    sqlite_db_path = "test_swap.db"
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)

    # 1. Instantiate the two different data layer repositories
    in_memory_repo = InMemoryBookRepository()
    sqlite_repo = SQLiteBookRepository(sqlite_db_path)
    
    # 2. Inject repositories into the Business Logic Manager
    manager_memory = BookManager(in_memory_repo)
    manager_sqlite = BookManager(sqlite_repo)
    
    # 3. Run the exact same sequence of operations on both managers
    run_business_logic(manager_memory, "InMemory Data Store")
    run_business_logic(manager_sqlite, "SQLite Data Store")

    # Cleanup test db
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)

if __name__ == "__main__":
    main()
