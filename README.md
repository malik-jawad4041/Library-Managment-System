# Library Management System

A simple Library Management System implemented in Python with PostgreSQL as the backend.  
This project allows managing books, members, and loans.

---

## **Features**

- Add, update, and manage books, members, and loans.
- Automatic handling of auto-increment IDs using PostgreSQL sequences.
- Uses environment variables for database configuration.

---

## **Setup Instructions**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/malik-jawad4041/Library-Managment-System.git
   cd Library-Managment-System

2. **Create virtual environment**
python -m venv assign1


3. **Install Dependencies**
pip install -r requirements.txt

4. **Create .env file and add followings**
DB_NAME=library_db
DB_USER=postgres
PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

5. **Execute SQL Script**
psql -U postgres -d library_db -f schema.sql

6. **How to run application**
source assign1/bin/activate      # Linux/macOS
assign1\Scripts\activate         # Windows

python main.py

7. **Assumptions made**
PostgreSQL is installed and running locally with Superuser credentials:
Username: postgres
Password: postgres

Environment variables are correctly set in .env for database connectivity.

