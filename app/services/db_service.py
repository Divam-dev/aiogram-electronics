import sqlite3

def get_category():
    """Get list of all product categories"""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM Products")
    categories = cursor.fetchall()
    conn.close()
    return list(set(category[0] for category in categories))

def get_products_by_category(category):
    """Get all products for a specific category"""
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
    """Get price for a specific product by name"""
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

def create_order(customer_id, product_id, quantity, total_price, delivery_method, status):
    """Create a new order record"""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO Orders 
        (customer_id, product_id, quantity, total_price, delivery_method, status) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, product_id, quantity, total_price, delivery_method, status))
    
    cursor.execute("""
        UPDATE Products 
        SET stock = stock - ? 
        WHERE id = ? AND stock >= ?
    """, (quantity, product_id, quantity))
    
    conn.commit()
    conn.close()
    
    return True

def update_customer_info(chat_id, phone=None, email=None, first_name=None, last_name=None):
    """Update customer information"""
    conn = sqlite3.connect('electronics_store.db')
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if phone:
        updates.append("phone_number = ?")
        params.append(phone)
        
    if email:
        updates.append("email = ?")
        params.append(email)
        
    if first_name:
        updates.append("first_name = ?")
        params.append(first_name)
        
    if last_name:
        updates.append("last_name = ?")
        params.append(last_name)
    
    if updates:
        query = f"UPDATE Customers SET {', '.join(updates)} WHERE chat_id = ?"
        params.append(chat_id)
        
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()
    return True