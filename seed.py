import requests
import uuid

API_URL = "http://127.0.0.1:8000/books"

books = [
    {"title": "Mastering the PERN Stack", "author": "Alex Web", "isbn": "1234567890", "publication_year": 2023, "quantity": 5},
    {"title": "Quantum Computing with Cirq", "author": "Quinn Qubit", "isbn": "0987654321", "publication_year": 2024, "quantity": 3},
    {"title": "Algorithmic Trading Strategies", "author": "Jordan Quant", "isbn": "1122334455", "publication_year": 2025, "quantity": 10},
    {"title": "Time-Series Forecasting Models", "author": "Dr. Data", "isbn": "5544332211", "publication_year": 2022, "quantity": 7},
    {"title": "Advanced PostgreSQL Integration", "author": "DB Admin", "isbn": "9988776655", "publication_year": 2023, "quantity": 12},
    {"title": "C++ Network Programming", "author": "Socket Master", "isbn": "5566778899", "publication_year": 2021, "quantity": 4},
    {"title": "CMOS VLSI Design Principles", "author": "Silicon Expert", "isbn": "1029384756", "publication_year": 2020, "quantity": 8},
    {"title": "Smart Money Concepts in Forex", "author": "Pip Trader", "isbn": "5647382910", "publication_year": 2024, "quantity": 15},
    {"title": "Data Structures in Python", "author": "Code Ninja", "isbn": "1357924680", "publication_year": 2022, "quantity": 20},
    {"title": "Building REST APIs with FastAPI", "author": "API Builder", "isbn": "0864297531", "publication_year": 2025, "quantity": 6},
    {"title": "React Frontend Architecture", "author": "UI Designer", "isbn": "1111222233", "publication_year": 2023, "quantity": 9},
    {"title": "TimescaleDB for Analytics", "author": "Query Pro", "isbn": "3333444455", "publication_year": 2024, "quantity": 2},
    {"title": "Docker Containerization", "author": "Ship It", "isbn": "5555666677", "publication_year": 2021, "quantity": 11},
    {"title": "GitHub Actions CI/CD", "author": "Auto Mate", "isbn": "7777888899", "publication_year": 2025, "quantity": 14},
    {"title": "Machine Learning with Scikit-Learn", "author": "Model Maker", "isbn": "9999000011", "publication_year": 2022, "quantity": 18},
    {"title": "PennyLane Quantum Circuits", "author": "Photon Logic", "isbn": "1212121212", "publication_year": 2024, "quantity": 5},
    {"title": "Pine Script for TradingView", "author": "Chart Reader", "isbn": "3434343434", "publication_year": 2023, "quantity": 7},
    {"title": "TCP/IP Congestion Control", "author": "Net Admin", "isbn": "5656565656", "publication_year": 2019, "quantity": 3},
    {"title": "Applied Neural Networks", "author": "Deep Learner", "isbn": "7878787878", "publication_year": 2025, "quantity": 13},
    {"title": "Pass Transistor Logic", "author": "Circuit Board", "isbn": "9090909090", "publication_year": 2020, "quantity": 6}
]

def seed_database():
    print(f"Starting seed process to {API_URL}...\n")
    success_count = 0
    failure_count = 0
    
    for book in books:
        # Generate a unique ID since our dataclass requires it
        book['id'] = str(uuid.uuid4())
        
        try:
            response = requests.post(API_URL, json=book)
            if response.status_code == 201:
                print(f"✅ SUCCESS: Added '{book['title']}' by {book['author']}")
                success_count += 1
            else:
                print(f"❌ FAILURE: Could not add '{book['title']}'. Status: {response.status_code}. Response: {response.text}")
                failure_count += 1
        except Exception as e:
            print(f"❌ ERROR: Failed to connect while adding '{book['title']}': {str(e)}")
            failure_count += 1
            
    print(f"\nSeed Complete! Successfully added {success_count} books. Failed to add {failure_count} books.")

if __name__ == "__main__":
    seed_database()
