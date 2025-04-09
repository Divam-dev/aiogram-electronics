import sqlite3
import requests

def currency_convert():
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5') 
    data = response.json()
    usd_price = next(item["sale"] for item in data if item["ccy"] == "USD")
    return usd_price

def get_category():
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM Products")
    categories = cursor.fetchall()
    conn.close()
    return list(set(category[0] for category in categories))

def get_products_by_category(category):
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE category = ?", (category,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    """Fetch a product by its ID from the database."""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_product_price(product_name):
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM Products WHERE name = ?", (product_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return float(result[0]) 
    return 0

def customer_exists(chat_id):
    """Check if a customer with the given chat_id already exists."""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Customers WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_customer_by_chat_id(chat_id):
    """Fetch customer data by chat_id."""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers WHERE chat_id = ?", (chat_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def add_new_customer(chat_id, first_name, last_name=None):
    """Add a new customer to the database."""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Customers (chat_id, first_name, last_name) VALUES (?, ?, ?)",
        (chat_id, first_name, last_name)
    )
    conn.commit()
    conn.close()