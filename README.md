# N-Tier Library Management Application

Welcome to the N-Tier Library Management system! This project demonstrates a strict implementation of a 3-tier architecture, designed to provide clear separation of concerns, robust business rule validation, and seamless data layer interchangeability. It fulfills all requirements outlined in the "Building a Simple N-Tier Application" assignment rubric.

---

## 🏗 Architecture Breakdown

The application is rigorously divided into three distinct layers, ensuring that no layer improperly communicates with or relies on the internal implementation of another.

### 1. Presentation Tier (`/presentation` & `/frontend`)
**Responsibility:** Handling Input/Output and User Interface exclusively.
- **Frontend:** A modern, highly interactive React SPA styled with Tailwind CSS v4. It manages state and provides a clean dashboard layout.
- **Backend (API):** A FastAPI REST backend (`app.py`) that strictly handles HTTP routing, request parsing, and response serialization.
- **Constraint Met:** This tier contains absolutely **zero** business validation rules and makes **zero** direct calls to any database libraries.

### 2. Business Logic Tier (`/business`)
**Responsibility:** The core orchestrator and enforcer of business rules.
- **BookManager:** The central class that processes all incoming requests from the presentation tier.
- **Rules Enforced:** 
  - Title and Author cannot be empty.
  - Publication Year cannot be in the future.
  - ISBN must be exactly 10 or 13 digits.
  - Quantity cannot be negative.
  - A book cannot be checked out if the quantity is 0 (raises a meaningful `CheckoutError` instead of crashing).
- **Constraint Met:** The business tier is entirely decoupled from the UI and Data implementations. It only interacts with the data tier through abstract interfaces.

### 3. Data Access Tier (`/data`)
**Responsibility:** Pure data persistence and retrieval.
- **Implementations:** Contains a concrete `SQLiteBookRepository` and a mock `InMemoryBookRepository`.
- **Constraint Met:** This layer executes SQL queries and manages data structures, but contains no business validation logic and has no knowledge of how the data will be displayed.

---

## 💡 Design Decision: The Repository Interface Pattern

To achieve true loose coupling between the Business and Data tiers, I utilized the **Repository Interface Pattern**. The Business logic (`BookManager`) relies exclusively on an abstract `BookRepository` class rather than importing `sqlite3` directly. This decision was critical because it allowed us to effortlessly swap the actual data source. For example, during unit testing and in our `swap_test.py` script, we were able to inject an `InMemoryBookRepository` (a fake data source using standard Python dictionaries). This means the business logic could be rigorously tested in isolation without hitting a real database or changing a single line of business tier code, perfectly proving the resilience of the architecture.

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
|       Presentation Tier         | (FastAPI, REST Endpoints, Routing)
|                                 |
+---------------+-----------------+
                | 
           (DTOs/Models)
                |
                v
+---------------+-----------------+
|                                 |
|         Business Tier           | (BookManager, Validation, Rules)
|                                 |
+---------------+-----------------+
                | 
      (Repository Interface)
                |
                v
+---------------+-----------------+
|                                 |
|           Data Tier             | (SQLiteBookRepository, InMemoryRepo)
|                                 |
+---------------------------------+
```

---

## 🚀 Setup & Execution Instructions

Follow these steps to run the application locally on your machine.

### 1. Install Dependencies
Open your terminal at the root of the project and install the required Python packages:
```bash
pip install fastapi uvicorn pydantic requests pytest
```
Then, install the React frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

### 2. Run the FastAPI Backend
Start the backend server from the root directory:
```bash
uvicorn presentation.app:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can explore the interactive Swagger UI at `http://127.0.0.1:8000/docs`.

### 3. Run the React Frontend
Open a **new** terminal, navigate to the `frontend` directory, and start the Vite development server:
```bash
cd frontend
npm run dev
```
The frontend will typically run at `http://localhost:5173`.

### 4. Seed the Database
To populate the UI with 20 mock tech books, open another terminal at the root directory and run:
```bash
python seed.py
```

---

## 🧪 Testing Instructions

The architecture's loose coupling allows for robust, isolated testing. Run the following from the root directory:

### Unit Tests
To verify that all business rules (negative quantities, invalid ISBNs, checkout limits) are correctly enforced in the business tier *without* hitting a real database:
```bash
PYTHONPATH=. pytest tests/
```

### The Swap Test
To prove that the Business logic operates identically regardless of the underlying data layer, run:
```bash
python swap_test.py
```
This script runs the exact same sequence of business operations on both the SQLite database and the In-Memory mock dictionary side-by-side, demonstrating seamless data-layer independence.