# Ice Cream Scoop Inventory - Streamlit + SQLite App

import streamlit as st
import sqlite3
from datetime import datetime

# -------------------- DATABASE SETUP --------------------
DB_NAME = 'scoop_inventory.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scoops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            branch TEXT,
            product_name TEXT,
            quantity INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_scoop(date, branch, product_name, quantity):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO scoops (date, branch, product_name, quantity) VALUES (?, ?, ?, ?)",
              (date, branch, product_name, quantity))
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

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Ice Cream Scoop Inventory", layout="centered")
st.title("🍨 Ice Cream Scoop Inventory")

init_db()

# Add new record
st.subheader("Add Scoop Record")
date = st.date_input("Date", datetime.now())
branch = st.selectbox("Branch", ["Main", "Masif", "Downtown", "Other"])
product = st.text_input("Product Name")
quantity = st.number_input("Quantity", min_value=1, step=1)

if st.button("Add Record"):
    if product:
        insert_scoop(str(date), branch, product, quantity)
        st.success("✅ Record added successfully")
    else:
        st.error("❌ Please enter a product name")

# View all records
st.subheader("📋 All Scoop Records")
data = get_all_scoops()
if data:
    for row in data:
        st.write(f"📌 {row[1]} | Branch: {row[2]} | Product: {row[3]} | Qty: {row[4]}")
        if st.button(f"❌ Delete", key=f"delete_{row[0]}"):
            delete_scoop(row[0])
            st.experimental_rerun()
else:
    st.info("No scoop records found yet.")
