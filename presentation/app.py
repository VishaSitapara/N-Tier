from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from data.models import Book
from data.sqlite_repo import SQLiteBookRepository
from business.book_manager import BookManager, ValidationError, CheckoutError, NotFoundError

# Setup and Injection
app = FastAPI(title="Library Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
repository = SQLiteBookRepository("library.db")
book_manager = BookManager(repository)

@app.post("/books", status_code=201)
def add_book(book: Book):
    try:
        book_manager.add_book(book)
        return {"message": "Book added successfully."}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books", response_model=List[Book])
def get_all_books():
    return book_manager.get_all_books()

@app.get("/books/search", response_model=List[Book])
def search_books(q: str = Query(..., description="Search query for title or author")):
    return book_manager.search_books(q)

@app.put("/books/{book_id}")
def update_book(book_id: str, book: Book):
    # Basic input routing check (not a business rule, just routing integrity)
    if str(book.id) != str(book_id):
        raise HTTPException(status_code=400, detail="Path ID does not match request body ID.")
        
    try:
        book_manager.update_book(book)
        return {"message": "Book updated successfully."}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    try:
        book_manager.delete_book(book_id)
        return {"message": "Book deleted successfully."}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/books/{book_id}/checkout")
def checkout_book(book_id: str):
    try:
        book_manager.checkout_book(book_id)
        return {"message": "Book checked out successfully."}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CheckoutError as e:
        raise HTTPException(status_code=400, detail=str(e))
