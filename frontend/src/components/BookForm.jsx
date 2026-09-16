import { useState } from 'react';

export default function BookForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    id: '',
    title: '',
    author: '',
    isbn: '',
    publication_year: '',
    quantity: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'publication_year' || name === 'quantity' ? (value === '' ? '' : Number(value)) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Generate a simple ID for the demo if not provided by user
    const submissionData = {
      ...formData,
      id: formData.id || Date.now().toString()
    };
    onSubmit(submissionData);
    // Clear form after submission attempt
    setFormData({ id: '', title: '', author: '', isbn: '', publication_year: '', quantity: '' });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 space-y-5">
      <h2 className="text-2xl font-bold text-gray-800 border-b pb-2 mb-4">Add a New Book</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div className="md:col-span-2">
          <label className="block text-sm font-semibold text-gray-700 mb-1">Title</label>
          <input required type="text" name="title" value={formData.title} onChange={handleChange} className="block w-full rounded-lg border border-gray-300 shadow-sm p-2.5 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all" />
        </div>
        
        <div className="md:col-span-2">
          <label className="block text-sm font-semibold text-gray-700 mb-1">Author</label>
          <input required type="text" name="author" value={formData.author} onChange={handleChange} className="block w-full rounded-lg border border-gray-300 shadow-sm p-2.5 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all" />
        </div>
        
        <div className="md:col-span-2">
          <label className="block text-sm font-semibold text-gray-700 mb-1">ISBN (10 or 13 digits)</label>
          <input required type="text" name="isbn" value={formData.isbn} onChange={handleChange} className="block w-full rounded-lg border border-gray-300 shadow-sm p-2.5 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all" />
        </div>
        
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">Publication Year</label>
          <input required type="number" name="publication_year" value={formData.publication_year} onChange={handleChange} className="block w-full rounded-lg border border-gray-300 shadow-sm p-2.5 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all" />
        </div>
        
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-1">Quantity</label>
          <input required type="number" name="quantity" value={formData.quantity} onChange={handleChange} className="block w-full rounded-lg border border-gray-300 shadow-sm p-2.5 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all" />
        </div>
      </div>

      <button disabled={isLoading} type="submit" className="w-full mt-6 bg-blue-600 text-white font-medium py-3 px-4 rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
        {isLoading ? 'Adding Book...' : 'Add Book to Inventory'}
      </button>
    </form>
  );
}
