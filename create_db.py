import sqlite3

conn = sqlite3.connect('electronics_store.db')
cursor = conn.cursor()

# Create Products table
cursor.execute("""
CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    fullname TEXT,
    image_url TEXT
);
""")

# Create Customers table
cursor.execute("""
CREATE TABLE Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    phone_number TEXT,
    email TEXT
);
""")

# Create Orders table
cursor.execute("""
CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_method TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES Customers (id),
    FOREIGN KEY (product_id) REFERENCES Products (id)
);
""")

sample_products = [
    ("SAMSUNG Galaxy S25 Ultra", "Smartphones", 59999.99, 10, "SAMSUNG Galaxy S25 Ultra 12/512Gb Dual Sim Titanium Grey (SM-S938BZTGEUC)", "https://files.foxtrot.com.ua/PhotoNew/img_0_60_10654_0_1_QiLkht.webp"),
    ("APPLE iPhone 13", "Smartphones", 19999.99, 8, "APPLE iPhone 13 128GB Midnight (MLPF3HU/A)", "https://files.foxtrot.com.ua/PhotoNew/img_0_60_8299_5_1.webp"),
    ("MacBook Air M1", "Laptops", 34999.99, 5, "Ноутбук APPLE MacBook Air M1 13' 256GB Space Grey (MGN63UA/A)", "https://files.foxtrot.com.ua/PhotoNew/img_0_58_18009_0.webp"),
    ("ACER Extensa 15", "Laptops", 18999.99, 2, "Ноутбук ACER Extensa 15 EX215-55-3564 Shale Black (NX.EGYEU.02J)", "https://files.foxtrot.com.ua/PhotoNew/img_0_58_27110_0_1_f2cSGZ.webp"),
    ("AirPods 4", "Headphones", 7449.99, 15, "Гарнітура APPLE AirPods 4 (MXP63ZE/A)", "https://files.foxtrot.com.ua/PhotoNew/img_0_564_6846_0_1_rPnuCC.webp"),
    ("JBL T110", "Headphones", 349.99, 50, "Гарнітура JBL T110 Black (JBLT110BLK)", "https://files.foxtrot.com.ua/PhotoNew/img_0_564_3225_0.webp"),
]

cursor.executemany("""
INSERT INTO Products (name, category, price, stock, fullname, image_url)
VALUES (?, ?, ?, ?, ?, ?);
""", sample_products)

# Commit changes and close connection
conn.commit()
conn.close()
