import sqlite3
from datetime import datetime

def insert_orders_raw_sql():
    conn = sqlite3.connect("khkr.db")
    cursor = conn.cursor()

    now = datetime.utcnow()

    orders = [
        ("ORD-007", "David King", now, 180.00, "Card", "Pending", now, now, 1),
        ("ORD-008", "Emily Rose", now, 220.00, "Net Banking", "Delivered", now, now, 1),
        ("ORD-009", "Frank Stone", now, 125.00, "Cash", "Processing", now, now, 1),
        ("ORD-010", "Grace Lee", now, 120.50, "UPI", "Pending", now, now, 1),
        ("ORD-011", "Henry Ford", now, 300.00, "Credit Card", "Delivered", now, now, 1),
        ("ORD-012", "Isla Fisher", now, 450.00, "PayPal", "Processing", now, now, 1),
        ("ORD-013", "Jake Paul", now, 75.00, "Cash", "Cancelled", now, now, 1),
        ("ORD-014", "Kelly Clarkson", now, 210.20, "Debit Card", "Delivered", now, now, 1),
        ("ORD-015", "Leo Messi", now, 980.99, "UPI", "Pending", now, now, 1),
        ("ORD-016", "Mia Wong", now, 310.75, "PayPal", "Processing", now, now, 1),
        ("ORD-017", "Nate Diaz", now, 89.00, "Net Banking", "Pending", now, now, 1),
        ("ORD-018", "Olivia Pope", now, 600.00, "Credit Card", "Delivered", now, now, 1),
        ("ORD-019", "Paul Rudd", now, 440.00, "Cash", "Processing", now, now, 1),
        ("ORD-020", "Quincy Adams", now, 150.00, "Cash", "Cancelled", now, now, 1),
        ("ORD-021", "Rachel Green", now, 340.00, "PayPal", "Delivered", now, now, 1),
        ("ORD-022", "Steve Jobs", now, 999.99, "UPI", "Processing", now, now, 1),
        ("ORD-023", "Tom Hanks", now, 180.75, "Debit Card", "Pending", now, now, 1),
        ("ORD-024", "Uma Thurman", now, 250.00, "Credit Card", "Delivered", now, now, 1),
        ("ORD-025", "Victor Hugo", now, 310.00, "Cash", "Pending", now, now, 1),
        ("ORD-026", "Wendy Wu", now, 405.00, "Net Banking", "Processing", now, now, 1),
        ("ORD-027", "Xander Cage", now, 215.00, "PayPal", "Cancelled", now, now, 1),
        ("ORD-028", "Yara Shahidi", now, 520.20, "Credit Card", "Delivered", now, now, 1),
        ("ORD-029", "Zack Snyder", now, 275.00, "UPI", "Pending", now, now, 1),
    ]

    try:
        cursor.executemany("""
            INSERT INTO orders (
                order_number, customer_name, order_date, amount, payment_method, status, created_at, updated_at, user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, orders)
        conn.commit()
        print(f"{len(orders)} orders inserted using raw SQL for user_id=1")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()


def insert_orders_raw_sql_invoice():
    conn = sqlite3.connect("khkr.db")
    cursor = conn.cursor()

    # Sample invoice data
    invoices = [
        ("#526534", "Kathryn Murphy", "2024-01-25", 200.00, "Delivered"),
        ("#696589", "Annette Black", "2024-01-25", 200.00, "Delivered"),
        ("#256584", "Ronald Richards", "2024-02-10", 200.00, "Delivered"),
        ("#526587", "Eleanor Pena", "2024-02-10", 200.00, "Processing"),
        ("#105986", "Leslie Alexander", "2024-03-15", 200.00, "Pending"),
        ("#526589", "Albert Flores", "2024-03-15", 200.00, "Cancelled"),
        ("#526520", "Jacob Jones", "2024-04-27", 200.00, "Delivered"),
        ("#256584", "Jerome Bell", "2024-04-27", 200.00, "Pending"),
        ("#200257", "Marvin McKinney", "2024-04-30", 200.00, "Processing"),
        ("#526525", "Cameron Williamson", "2024-04-30", 200.00, "Delivered"),
    ]

    # Connect to the database and insert data
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # Create the invoices table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT,
        customer_name TEXT,
        issued_date TEXT,
        amount REAL,
        status TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    # Add timestamps and insert the data
    now = datetime.utcnow().isoformat()
    invoice_entries = [(i[0], i[1], i[2], i[3], i[4], now, now) for i in invoices]

    cursor.executemany("""
    INSERT INTO invoices (
        invoice_number, customer_name, issued_date, amount, status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, invoice_entries)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # insert_orders_raw_sql()
    insert_orders_raw_sql_invoice()