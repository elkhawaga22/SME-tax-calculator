import streamlit as st
import pandas as pd
import requests

# --- 1. Configuration ---
API_KEY = "AIzaSyCULRB3xyOnO9f87qoUVYsSUhqa9yrQRNE"

# --- 2. Page Config ---
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("SME Tax Expert")
st.sidebar.markdown("Graduation Project 2026") 

page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", 
    "2. Operating Expenses", 
    "3. Tax Dashboard & Report",
    "4. Smart Tax Assistant 🤖",
    "5. About the Project"
])

# ==========================
# 1. Sales Module (نفس الكود)
# ==========================
if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management Module")
    with st.form("add_sale"):
        c1, c2 = st.columns(2)
        client = c1.text_input("Client Name")
        amt = c2.number_input("Invoice Amount (EGP)", min_value=0.0)
        if st.form_submit_button
