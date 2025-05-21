# database.py

import sqlite3
from config import DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scoops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            branch TEXT,
            product_name TEXT,
            unit TEXT,
            quantity INTEGER,
            price_iqd INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_scoop(date, branch, product_name, unit, quantity, price_iqd):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO scoops (date, branch, product_name, unit, quantity, price_iqd) VALUES (?, ?, ?, ?, ?, ?)",
              (date, branch, product_name, unit, quantity, price_iqd))
    conn.commit()
    conn.close()

def get_all_scoops():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM scoops ORDER BY date DESC")
    data = c.fetchall()
    conn.close()
    return data

def delete_scoop(record_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM scoops WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def update_scoop(record_id, date, branch, product_name, unit, quantity, price_iqd):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE scoops SET date=?, branch=?, product_name=?, unit=?, quantity=?, price_iqd=? WHERE id=?
    """, (date, branch, product_name, unit, quantity, price_iqd, record_id))
    conn.commit()
    conn.close()
