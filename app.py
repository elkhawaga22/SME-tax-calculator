import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="SME Mini ERP", layout="wide")

# --- Database Simulation (Session State) ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state:
    st.session_state.expenses_data = []

# --- Sidebar Menu ---
st.sidebar.title("🏢 SME ERP System")
page = st.sidebar.radio("Main Menu", ["1. Sales & Invoicing", "2. Operating Expenses", "3. Financial Position & Tax"])

# ==========================
# 1. Sales Module
# ==========================
if page == "1. Sales & Invoicing":
    st.header("🛒 Sales Management")
    
    # Invoice Entry Form
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client_name = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0, step=100.0)
        submit_sale = st.form_submit_button("Save Invoice")
        
        if submit_sale and amount > 0:
            st.session_state.sales_data.append({"Client": client_name, "Amount": amount})
            st.success("Invoice saved successfully! ✅")

    # Display Sales Log
    if st.session_state.sales_data:
        st.subheader("Invoices Log")
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df_sales, use_container_width=True)
        st.metric("Total Revenue", f"EGP {df_sales['Amount'].sum():,.2f}")
    else:
        st.info("No sales recorded yet.")

# ==========================
# 2. Expenses Module
# ==========================
elif page == "2. Operating Expenses":
    st.header("💸 Expense Management")
    
    # Expense Entry Form
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        desc =