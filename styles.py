# styles.py

import streamlit as st

def inject_font():
    font_url = "https://www.kurdfonts.com/uploads/files/2023-11/1700141447_zarif.ttf"
    st.markdown(f"""
        <style>
        @font-face {{
            font-family: 'Zarif';
            src: url('{font_url}') format('truetype');
        }}
        html, body, [class^="css"] {{
            font-family: 'Zarif', sans-serif;
        }}
        </style>
    """, unsafe_allow_html=True)

def apply_theme(mode="Light"):
    if mode == "Dark":
        st.markdown("""
            <style>
            body, .stApp {{
                background-color: #121212;
                color: #f1f1f1;
            }}
            </style>
        """, unsafe_allow_html=True)
