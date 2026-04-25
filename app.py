import streamlit as st
import pandas as pd

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state:
    st.session_state.expenses_data = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("SME Tax Expert")
page = st.sidebar.radio("القوائم", ["المبيعات", "المصروفات", "الضرائب", "الفريق"])

# 1. Sales
if page == "المبيعات":
    st.title("Sales & Invoicing")
    with st.form("sales"):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client")
        amount = col2.number_input("Amount", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("Saved!")
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df)
        st.metric("Total", df['Amount'].sum())
    
    if st.button("Clear"):
        st.session_state.sales_data = []
        st.rerun()

# 2. Expenses
elif page == "المصروفات":
    st.title("Operating Expenses")
    with st.form("exp"):
        col1, col2 = st.columns(2)
        item = col1.text_input("Item")
        cost = col2.number_input("Cost", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("Saved!")
            st.rerun()
    
    if st.session_state.expenses_data:
        df = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df)
        st.metric("Total", df['Cost'].sum())
    
    if st.button("Clear"):
        st.session_state.expenses_data = []
        st.rerun()

# 3. Tax Dashboard
elif page == "الضرائب":
    st.title("Tax Dashboard")
    sales = sum(d['Amount'] for d in st.session_state.sales_data)
    expenses = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = sales - expenses
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Sales", sales)
    col2.metric("Expenses", expenses)
    col3.metric("Profit", profit)
    
    st.subheader("Tax Calculations")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Law 152")
        tax152 = 5000 if sales < 1000000 else sales * 0.01
        st.success(f"EGP {tax152:,.0f}")
    with col2:
        st.warning("Law 91")
        tax91 = max(0, profit * 0.225)
        st.warning(f"EGP {tax91:,.0f}")

# 4. Team - بدون markdown كبير
elif page == "الفريق":
    st.title("Team")
    st.write("Omar Mohamed Ahmed - 2202297")
    st.write("Mennatallah Moamen - 2200216")
    st.write("Mareez Adham - 2200243")
    st.write("Basmala Mohamed Saad - 2200236")
    st.balloons()
    
