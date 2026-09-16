const BASE_URL = 'http://localhost:8000/books';

async function handleResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || 'An unexpected error occurred');
  }
  return data;
}

export const api = {
  getBooks: () => fetch(BASE_URL).then(handleResponse),
  
  searchBooks: (query) => fetch(`${BASE_URL}/search?q=${encodeURIComponent(query)}`).then(handleResponse),
  
  addBook: (bookData) => fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookData)
  }).then(handleResponse),
  
  checkoutBook: (id) => fetch(`${BASE_URL}/${id}/checkout`, {
    method: 'POST'
  }).then(handleResponse),
  
  deleteBook: (id) => fetch(`${BASE_URL}/${id}`, {
    method: 'DELETE'
  }).then(handleResponse)
};
