export default function BookCard({ book, onCheckout, onDelete, isProcessing }) {
  const isOutOfStock = book.quantity <= 0;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-full hover:shadow-md transition-shadow">
      <div className="p-6 flex-grow">
        <h3 className="text-lg font-bold text-gray-900 leading-tight mb-1">{book.title}</h3>
        <p className="text-sm font-medium text-gray-500 mb-4">by {book.author}</p>
        
        <div className="space-y-1.5 text-sm text-gray-600">
          <p><span className="font-semibold text-gray-700">ISBN:</span> {book.isbn}</p>
          <p><span className="font-semibold text-gray-700">Year:</span> {book.publication_year}</p>
          <div className="pt-2 mt-2 border-t border-gray-100">
            <span className="font-semibold text-gray-700">Stock:</span>{' '}
            <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${isOutOfStock ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
              {isOutOfStock ? 'OUT OF STOCK' : `${book.quantity} AVAILABLE`}
            </span>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-50 p-4 border-t border-gray-200 flex space-x-3">
        <button 
          onClick={() => onCheckout(book.id)}
          disabled={isOutOfStock || isProcessing}
          className="flex-1 bg-emerald-600 text-white font-medium py-2 px-4 rounded-lg shadow-sm transition-colors hover:bg-emerald-700 focus:ring-2 focus:ring-emerald-500 disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed"
        >
          Check Out
        </button>
        <button 
          onClick={() => onDelete(book.id)}
          disabled={isProcessing}
          className="bg-white border border-red-200 text-red-600 font-medium py-2 px-4 rounded-lg shadow-sm transition-colors hover:bg-red-50 hover:border-red-300 focus:ring-2 focus:ring-red-500 disabled:opacity-50"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
