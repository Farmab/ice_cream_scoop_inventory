# main.py

import streamlit as st
from datetime import datetime
import pandas as pd
from database import *
from styles import inject_font, apply_theme
from config import DEFAULT_UNITS, BRANCHES

st.set_page_config(page_title="🍦 Ice Cream Scoop Inventory", layout="centered")
inject_font()

# Theme switcher
theme = st.radio("🌓 Theme Mode", ["Light", "Dark"], horizontal=True)
apply_theme(theme)

st.title("🍦 Ice Cream Scoop Inventory")

init_db()

# ----- Add Record -----
st.subheader("➕ Add Scoop Record")

date = st.date_input("Date", datetime.now())
branch = st.selectbox("Branch", BRANCHES)
product = st.text_input("Product Name")

# Unit selection
selected_unit = st.selectbox("Select Unit", DEFAULT_UNITS + ["Other"])
unit = st.text_input("Enter new unit") if selected_unit == "Other" else selected_unit

quantity = st.number_input("Quantity", min_value=1, step=1)
price_iqd = st.number_input("Price (IQD)", min_value=0, step=100)

if st.button("Add Record"):
    if product and unit:
        insert_scoop(str(date), branch, product, unit, quantity, price_iqd)
        st.success("✅ Record added successfully.")
    else:
        st.error("❌ Please fill all fields.")

# Go to reports
st.markdown("---")
if st.button("📊 Go to Reports & Filter"):
    st.switch_page("report_section.py")
