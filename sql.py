
import sqlite3


conn = sqlite3.connect('company_sales.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS cust (
        custid INTEGER PRIMARY KEY,
        custname TEXT NOT NULL,
        location TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS company (
        companyid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        sector TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        prodid INTEGER PRIMARY KEY,
        companyid INTEGER,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (companyid) REFERENCES company(companyid)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        salesid INTEGER PRIMARY KEY,
        custid INTEGER,
        prodid INTEGER,
        qty INTEGER NOT NULL,
        price REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (custid) REFERENCES cust(custid),
        FOREIGN KEY (prodid) REFERENCES products(prodid)
    )
''')

cust_data = [
    (1, 'John Doe', 'New York'),
    (2, 'Jane Smith', 'Los Angeles'),
    (3, 'Alice Johnson', 'Chicago'),
    (4, 'Robert Brown', 'Houston'),
    (5, 'Michael Davis', 'Phoenix'),
    (6, 'Mary Garcia', 'Philadelphia'),
    (7, 'William Martinez', 'San Antonio'),
    (8, 'Linda Rodriguez', 'San Diego'),
    (9, 'David Hernandez', 'Dallas'),
    (10, 'Barbara Lopez', 'San Jose')
]
cursor.executemany('INSERT OR IGNORE INTO cust VALUES (?, ?, ?)', cust_data)

company_data = [
    (1, 'TechCorp', 'Technology'),
    (2, 'HealthPlus', 'Healthcare'),
    (3, 'EduWorld', 'Education'),
    (4, 'Foodies', 'Food & Beverage'),
    (5, 'AutoMakers', 'Automotive'),
    (6, 'FinanceWorks', 'Finance'),
    (7, 'TravelTime', 'Travel'),
    (8, 'RetailKing', 'Retail'),
    (9, 'EnergyGen', 'Energy'),
    (10, 'MediaHub', 'Media')
]
cursor.executemany('INSERT OR IGNORE INTO company VALUES (?, ?, ?)', company_data)

products_data = [
    (1, 1, 'Package Material', 199.99),
    (2, 1, 'Bolts', 29.99),
    (3, 2, 'Saw', 49.99),
    (4, 4, 'Cloth', 15.99),
    (5, 4, 'Alkali', 23999.99),
    (6, 6, 'Fertilizer', 19.99),
    (7, 6, 'Salt', 799.99),
    (8, 8, 'Aromatics', 49.99),
    (9, 9, 'Circuit Equip', 99.99),
    (10, 1, 'DC Regulator', 9.99)
]
cursor.executemany('INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)', products_data)

sales_data = [
    (1, 1, 1, 2, 399.98, '2023-01-15'),
    (2, 2, 2, 1, 29.99, '2023-02-28'),
    (3, 3, 3, 5, 249.95, '2023-03-20'),
    (4, 4, 4, 3, 47.97, '2023-04-10'),
    (5, 5, 5, 1, 23999.99, '2023-05-05'),
    (6, 6, 6, 10, 199.90, '2023-06-15'),
    (7, 7, 7, 1, 799.99, '2023-07-20'),
    (8, 8, 8, 4, 199.96, '2023-08-25'),
    (9, 9, 9, 2, 199.98, '2023-09-30'),
    (10, 10, 10, 6, 59.94, '2023-10-12')
]
cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', sales_data)

conn.commit()
conn.close()

print("Database tables created and data inserted successfully.")
