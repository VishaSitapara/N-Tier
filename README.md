# Three-Tier Library Management Application

Welcome to the Library Management system! This project showcases a structured 3-tier architecture with a clear separation of responsibilities, strong business-rule validation, and interchangeable data-layer implementations. It satisfies the requirements specified in the "Building a Simple N-Tier Application" assignment rubric.

---

## 🏗 Architecture Overview

The application is organized into three clearly separated layers, with each layer communicating through defined boundaries rather than depending on another layer's internal implementation.

### 1. Presentation Tier (`/presentation` & `/frontend`)
**Responsibility:** Managing user interaction, input, and output.
- **Frontend:** A modern React SPA built with Tailwind CSS v4. It handles application state and presents the functionality through a clean dashboard interface.
- **Backend (API):** A FastAPI REST backend (`app.py`) responsible for HTTP routing, request parsing, and response serialization.
- **Constraint Met:** This tier contains **no** business validation rules and does not make **direct** calls to database libraries.

### 2. Business Logic Tier (`/business`)
**Responsibility:** Coordinating application operations and enforcing business rules.
- **BookManager:** The main class responsible for handling requests received from the presentation tier.
- **Rules Enforced:**
  - Title and Author must not be empty.
  - Publication Year must not be a future year.
  - ISBN must contain exactly 10 or 13 digits.
  - Quantity must not be negative.
  - A book cannot be checked out when its quantity is 0; a meaningful `CheckoutError` is raised instead of allowing the application to crash.
- **Constraint Met:** The business tier remains independent of the UI and concrete data implementations. Communication with the data tier occurs only through abstract interfaces.

### 3. Data Access Tier (`/data`)
**Responsibility:** Handling data storage and retrieval.
- **Implementations:** Provides a concrete `SQLiteBookRepository` along with a mock `InMemoryBookRepository`.
- **Constraint Met:** This layer handles SQL queries and data structures, while remaining free of business validation logic and presentation concerns.

---

## 💡 Design Decision: Repository Interface Pattern

To keep the Business and Data tiers loosely coupled, the project uses the **Repository Interface Pattern**. The Business logic (`BookManager`) depends only on the abstract `BookRepository` class instead of directly importing `sqlite3`. This makes it possible to replace the underlying data source easily. For instance, during unit testing and in `swap_test.py`, an `InMemoryBookRepository` can be injected as a mock data source backed by standard Python dictionaries. As a result, the business logic can be tested independently without accessing a real database or modifying the business-tier code, demonstrating the flexibility of the architecture.

---

## 🗺 Architecture Diagram

```text
       [React / Tailwind UI]
                 |
            (HTTP / JSON)
                 |
                 v
+---------------------------------+
|                                 |
|       Presentation Tier         | (FastAPI, REST Endpoints, Request Handling)
|                                 |
+---------------+-----------------+
                | 
           (DTOs/Models)
                |
                v
+---------------+-----------------+
|                                 |
|         Business Tier           | (BookManager, Validation, Business Rules)
|                                 |
+---------------+-----------------+
                | 
      (Repository Interface)
                |
                v
+---------------+-----------------+
|                                 |
|           Data Tier             | (SQLiteBookRepository, InMemoryRepository)
|                                 |
+---------------------------------+
```

---

## 🚀 Setup & Execution Guide

Use the following steps to launch the application locally.

### 1. Install the Dependencies
From the project root, open a terminal and install the required Python packages:
```bash
pip install fastapi uvicorn pydantic requests pytest
```
Next, install the dependencies required by the React frontend:
```bash
cd frontend
npm install
cd ..
```

### 2. Start the FastAPI Backend
Launch the backend server from the project root:
```bash
uvicorn presentation.app:app --reload
```
The API will be accessible at `http://127.0.0.1:8000`. The interactive Swagger UI can be opened at `http://127.0.0.1:8000/docs`.

### 3. Start the React Frontend
Open a **new** terminal, move into the `frontend` directory, and start the Vite development server:
```bash
cd frontend
npm run dev
```
The frontend will normally be available at `http://localhost:5173`.

### 4. Populate the Database
To load the UI with 20 mock technology books, open another terminal at the project root and run:
```bash
python seed.py
```

---

## 🧪 Testing Guide

The loose coupling between the layers makes isolated testing straightforward. Run the following commands from the project root:

### Unit Testing
To confirm that the business tier correctly enforces all business rules (negative quantities, invalid ISBNs, and checkout limits) *without* connecting to a real database:
```bash
PYTHONPATH=. pytest tests/
```

### Swap Test
To demonstrate that the Business logic behaves the same way with different data-layer implementations, run:
```bash
python swap_test.py
```
This script performs the same sequence of business operations using both the SQLite database and the in-memory mock dictionary, showing that the business logic remains independent of the underlying data source.