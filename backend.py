import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="retail_store.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                barcode TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                is_service BOOLEAN DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_time TEXT,
                total_amount REAL
            )
        """)
        self.conn.commit()

    def seed_data(self):
        self.cursor.execute("SELECT count(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            items = [
                ("Молоко 3.2%", "1001", 85.00, 50, 0),
                ("Хлеб Бородинский", "1002", 45.50, 30, 0),
                ("Кофе (Стакан 0.3)", "2001", 150.00, 1000, 1),
                ("Пакет майка", "3001", 5.00, 500, 0)
            ]
            self.cursor.executemany("INSERT INTO products (name, barcode, price, stock, is_service) VALUES (?, ?, ?, ?, ?)", items)
            self.conn.commit()

    def get_product(self, barcode):
        self.cursor.execute("SELECT * FROM products WHERE barcode = ?", (barcode,))
        return self.cursor.fetchone()

    def add_product(self, name, barcode, price, stock, is_service):
        try:
            query = "INSERT INTO products (name, barcode, price, stock, is_service) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(query, (name, barcode, price, stock, is_service))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def process_sale(self, cart_items, total):
        try:
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO sales (date_time, total_amount) VALUES (?, ?)", (date_now, total))
            
            for item in cart_items:
                product_id = item['id']
                qty = item['qty']
                is_service = item['is_service']
                
                if not is_service:
                    self.cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, product_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def close(self):
        self.conn.close()
