# Ice Cream Scoop Inventory - Streamlit + SQLite App

import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import base64

# -------------------- STREAMLIT CONFIG (MUST BE FIRST) --------------------
st.set_page_config(page_title="Ice Cream Scoop Inventory", layout="centered")

# -------------------- CUSTOM FONT STYLE --------------------
def inject_custom_font():
    font_url = "https://www.kurdfonts.com/uploads/files/2023-11/1700141447_zarif.ttf"
    font_css = f"""
        <style>
        @font-face {{
            font-family: 'Zarif';
            src: url('{font_url}') format('truetype');
        }}
        html, body, [class^="css"]  {{
            font-family: 'Zarif', sans-serif;
        }}
        </style>
    """
    st.markdown(font_css, unsafe_allow_html=True)

inject_custom_font()

# -------------------- DATABASE SETUP --------------------
DB_NAME = 'scoop_inventory.db'

DEFAULT_UNITS = ["kg", "litre", "piece", "box", "carton", "rabta", "3alba"]

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

def upgrade_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE scoops ADD COLUMN unit TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE scoops ADD COLUMN price_iqd INTEGER")
    except sqlite3.OperationalError:
        pass
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

# -------------------- STREAMLIT UI --------------------
st.title("🍨 Ice Cream Scoop Inventory")

init_db()
upgrade_db()

# Add new record
st.subheader("Add Scoop Record")
date = st.date_input("Date", datetime.now())
branch = st.selectbox("Branch", ["Main", "Masif", "Downtown", "Other"])
product = st.text_input("Product Name")

# Select or add unit
unit_options = DEFAULT_UNITS.copy()
selected_unit = st.selectbox("Select Unit", unit_options + ["Other"])
if selected_unit == "Other":
    new_unit = st.text_input("Enter new unit")
    unit = new_unit if new_unit else ""
else:
    unit = selected_unit

quantity = st.number_input("Quantity", min_value=1, step=1)
price_iqd = st.number_input("Price (IQD)", min_value=0, step=100)

if st.button("Add Record"):
    if product and unit:
        insert_scoop(str(date), branch, product, unit, quantity, price_iqd)
        st.success("✅ Record added successfully")
    else:
        st.error("❌ Please enter all product details")

# Filtering/report section navigation
if st.button("📊 Go to Report & Filter Section"):
    st.switch_page("report_section.py")

# View all records
st.subheader("📋 All Scoop Records")
data = get_all_scoops()
if data:
    df = pd.DataFrame(data, columns=["ID", "Date", "Branch", "Product Name", "Unit", "Quantity", "Price (IQD)"])
    df["Total"] = df["Quantity"] * df["Price (IQD)"]
    total_revenue = df["Total"].sum()

    st.markdown(f"### 💰 Total Revenue: {total_revenue:,.0f} IQD")
    st.dataframe(df.style.set_properties(**{'border': '1px solid black'}), use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Export to CSV", data=csv, file_name="scoop_inventory.csv", mime="text/csv")

    for row in data:
        if st.button(f"✏️ Edit ID {row[0]}", key=f"edit_{row[0]}"):
            st.session_state.edit_id = row[0]
            st.session_state.edit_values = row
            st.experimental_rerun()
        if st.button(f"❌ Delete ID {row[0]}", key=f"delete_{row[0]}"):
            delete_scoop(row[0])
            st.experimental_rerun()

    # Inline editing form
    if "edit_id" in st.session_state:
        st.subheader("✏️ Edit Record")
        edit_id = st.session_state.edit_id
        r = st.session_state.edit_values
        new_date = st.date_input("Edit Date", datetime.strptime(r[1], "%Y-%m-%d"))
        new_branch = st.selectbox("Edit Branch", ["Main", "Masif", "Downtown", "Other"], index=["Main", "Masif", "Downtown", "Other"].index(r[2]))
        new_product = st.text_input("Edit Product Name", r[3])
        new_unit = st.text_input("Edit Unit", r[4])
        new_quantity = st.number_input("Edit Quantity", value=r[5], step=1)
        new_price = st.number_input("Edit Price (IQD)", value=r[6], step=100)
        if st.button("💾 Save Changes"):
            update_scoop(edit_id, str(new_date), new_branch, new_product, new_unit, new_quantity, new_price)
            del st.session_state.edit_id
            del st.session_state.edit_values
            st.success("Record updated successfully.")
            st.experimental_rerun()
        if st.button("❌ Cancel Edit"):
            del st.session_state.edit_id
            del st.session_state.edit_values
            st.experimental_rerun()
else:
    st.info("No scoop records found yet.")
