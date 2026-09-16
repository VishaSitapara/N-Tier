import { useState, useEffect } from 'react';
import { api } from './api';
import BookForm from './components/BookForm';
import BookCard from './components/BookCard';

function App() {
  const [books, setBooks] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Fetch all books on load
  const loadBooks = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getBooks();
      setBooks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, []);

  // Handle Search
  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (searchQuery.trim() === '') {
        loadBooks();
        return;
      }
      setIsLoading(true);
      try {
        const data = await api.searchBooks(searchQuery);
        setBooks(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }, 400); // 400ms debounce

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  const handleAddBook = async (bookData) => {
    setIsProcessing(true);
    setError(null);
    try {
      await api.addBook(bookData);
      await loadBooks(); // Refresh list to get updated inventory
    } catch (err) {
      setError(`Validation Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCheckout = async (id) => {
    setIsProcessing(true);
    setError(null);
    try {
      await api.checkoutBook(id);
      await loadBooks(); // Refresh list to get updated quantities
    } catch (err) {
      setError(`Checkout Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to permanently delete this book?')) return;
    setIsProcessing(true);
    setError(null);
    try {
      await api.deleteBook(id);
      await loadBooks(); // Refresh list
    } catch (err) {
      setError(`Delete Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-indigo-800 text-white py-8 shadow-lg">
        <div className="container mx-auto px-6 lg:px-12">
          <h1 className="text-4xl font-extrabold tracking-tight">N-Tier Library Manager</h1>
          <p className="mt-2 text-blue-200 text-lg font-medium">React Presentation Layer</p>
        </div>
      </header>

      <main className="container mx-auto px-6 lg:px-12 py-10">
        {/* Global Error Banner */}
        {error && (
          <div className="mb-8 bg-red-50 border-l-4 border-red-500 text-red-800 p-5 rounded-r-lg shadow-md flex items-start" role="alert">
            <svg className="w-6 h-6 mr-3 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <div>
              <p className="font-bold text-red-900">Operation Failed</p>
              <p className="mt-1">{error}</p>
            </div>
          </div>
        )}

        <div className="flex flex-col lg:flex-row gap-10">
          {/* Sidebar for Form */}
          <div className="w-full lg:w-1/3 flex-shrink-0">
            <div className="sticky top-10">
              <BookForm onSubmit={handleAddBook} isLoading={isProcessing} />
            </div>
          </div>

          {/* Main Grid for Cards */}
          <div className="w-full lg:w-2/3">
            <div className="mb-8">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search inventory by title or author..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-white rounded-xl border border-gray-200 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-lg transition-all"
                />
                <svg className="w-6 h-6 text-gray-400 absolute left-4 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              </div>
            </div>

            {isLoading ? (
              <div className="flex justify-center items-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : books.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-16 flex flex-col items-center justify-center text-gray-500">
                <svg className="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                <p className="text-2xl font-semibold text-gray-700">No books found</p>
                <p className="mt-2 text-center max-w-md">Try adjusting your search criteria or use the form to add a new book to the library.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {books.map(book => (
                  <BookCard 
                    key={book.id} 
                    book={book} 
                    onCheckout={handleCheckout} 
                    onDelete={handleDelete}
                    isProcessing={isProcessing}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
