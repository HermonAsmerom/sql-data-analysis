import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# --- Create database ---
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# --- Create tables ---
cursor.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT,
    signup_date TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

# --- Seed data ---
random.seed(42)

cities = ["London", "Manchester", "Birmingham", "Leeds", "Bristol", "Edinburgh"]
names = ["Alice Johnson", "Ben Carter", "Clara Smith", "David Lee", "Emma Brown",
         "Felix White", "Grace Hall", "Harry Young", "Isla King", "James Green",
         "Karen Scott", "Liam Adams", "Mia Baker", "Noah Clark", "Olivia Evans",
         "Paul Harris", "Quinn Walker", "Rachel Turner", "Sam Wilson", "Tara Lewis"]

customers = [(i+1, names[i], f"user{i+1}@email.com", random.choice(cities),
              (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"))
             for i in range(20)]
cursor.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", customers)

products = [
    (1, "Wireless Headphones", "Electronics", 79.99),
    (2, "Running Shoes", "Sports", 59.99),
    (3, "Coffee Maker", "Home", 49.99),
    (4, "Yoga Mat", "Sports", 29.99),
    (5, "Laptop Stand", "Electronics", 39.99),
    (6, "Water Bottle", "Sports", 19.99),
    (7, "Desk Lamp", "Home", 34.99),
    (8, "Bluetooth Speaker", "Electronics", 89.99),
    (9, "Protein Powder", "Health", 44.99),
    (10, "Smart Watch", "Electronics", 129.99),
]
cursor.executemany("INSERT INTO products VALUES (?,?,?,?)", products)

order_id = 1
item_id = 1
orders = []
order_items = []

for customer_id in range(1, 21):
    num_orders = random.randint(1, 4)
    for _ in range(num_orders):
        order_date = (datetime(2023, 6, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")
        status = random.choice(["completed", "completed", "completed", "returned", "pending"])
        orders.append((order_id, customer_id, order_date, status))

        num_items = random.randint(1, 3)
        for _ in range(num_items):
            product_id = random.randint(1, 10)
            quantity = random.randint(1, 3)
            order_items.append((item_id, order_id, product_id, quantity))
            item_id += 1
        order_id += 1

cursor.executemany("INSERT INTO orders VALUES (?,?,?,?)", orders)
cursor.executemany("INSERT INTO order_items VALUES (?,?,?,?)", order_items)

conn.commit()
conn.close()
print("✅ Database created: ecommerce.db")
