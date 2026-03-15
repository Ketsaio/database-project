# PostgreSQL Database Project

## Overview
This project is a practical implementation of a database-driven application developed to demonstrate proficiency in PostgreSQL and Python integration. It focuses on core database concepts including schema design, CRUD operations, and role-based access control.

## Project Goal
The primary objective of this repository is to showcase:
- Relational database modeling in PostgreSQL.
- Python-to-Postgres connectivity.
- Practical implementation of user roles (Admin vs. Client).
- Handling SQL queries and data manipulation through a Python interface.

## File Descriptions
- main.py: The main entry point of the application.
- signin.py: Handles user authentication and session startup.
- adm.py: Contains administrative functions (e.g., data management, reporting).
- client.py: Contains user-level functions (e.g., viewing records, basic interactions).
- generator.py: A utility script used to populate the Postgres tables with sample data.
- test_data.sql: The SQL source file containing the DDL (table structures) and DML (initial data inserts).
- req.txt: List of required Python libraries (e.g., psycopg2).

## Disclaimer
Some tables records is hardcoded to guarantee that all application responses remain meaningful and consistent:
- Category (Kategoria)
- Manufacturer (Producent)
- Product (Produkt)


## Database Setup
1. Ensure you have a PostgreSQL instance running.
2. Create a new database for the project.
3. Execute the commands found in `testowe_dane.sql` to build the schema:
   psql -d your_db_name -f testowe_dane.sql

## How to Run
1. Install dependencies:
   pip install -r req.txt
2. Configure your database connection strings within the Python files (if applicable).
3. Launch the application:
   python main.py

## Authors
Bartosz Kaczorowski

Anton Jędrzejewski

Developed as a database course verification project.