# report_section.py

import streamlit as st
import pandas as pd
from database import get_all_scoops
from styles import inject_font, apply_theme

st.set_page_config(page_title="📊 Reports", layout="wide")
inject_font()

theme = st.radio("🌓 Theme Mode", ["Light", "Dark"], horizontal=True)
apply_theme(theme)

st.title("📊 Reports & Filtering")

data = get_all_scoops()
if data:
    df = pd.DataFrame(data, columns=["ID", "Date", "Branch", "Product Name", "Unit", "Quantity", "Price (IQD)"])
    df["Total"] = pd.to_numeric(df["Quantity"], errors='coerce') * pd.to_numeric(df["Price (IQD)"], errors='coerce')
    total_revenue = df["Total"].sum()

    df["Total"] = df["Total"].apply(lambda x: f"{int(x):,} IQD")
    st.markdown(f"### 💰 Total Revenue: {int(total_revenue):,} IQD")
    st.dataframe(df, use_container_width=True)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Export CSV", csv, "scoop_inventory_report.csv", mime="text/csv")
else:
    st.info("No records available.")
