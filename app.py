import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# 1. AI Configuration
os.environ["GOOGLE_API_USE_MTLS"] = "never"
genai.configure(api_key="AIzaSyCULRB3xyOnO9f87qoUVYsSUhqa9yrQRNE")

# 2. Page Configuration & Styling
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# --- Database Simulation (Session State) ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state:
    st.session_state.expenses_data = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar Menu ---
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
# 1. Sales Module
# ==========================
if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management Module")
    st.markdown("Record your daily sales to track Gross Revenue.")
    
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client_name = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0, step=100.0)
        submit_sale = st.form_submit_button("💾 Save Invoice")
        
        if submit_sale and amount > 0:
            st.session_state.sales_data.append({"Client": client_name, "Amount": amount})
            st.success("Invoice saved successfully! ✅")

    if st.session_state.sales_data:
        st.divider()
        st.subheader("📋 Invoices Log")
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df_sales, use_container_width=True)
        st.metric("Total Revenue (Turnover)", f"EGP {df_sales['Amount'].sum():,.2f}")
    else:
        st.info("No sales recorded yet. Start by adding an invoice.")

# ==========================
# 2. Operating Expenses Module
# ==========================
elif page == "2. Operating Expenses":
    st.title("💸 Expense Management Module")
    st.markdown("Track operating costs to calculate Net Profit accurately.")
    
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        desc = col1.text_input("Expense Item (e.g., Rent, Salaries)")
        cost = col2.number_input("Cost (EGP)", min_value=0.0, step=100.0)
        submit_exp = st.form_submit_button("💾 Record Expense")
        
        if submit_exp and cost > 0:
            st.session_state.expenses_data.append({"Item": desc, "Cost": cost})
            st.success("Expense recorded successfully! ✅")

    if st.session_state.expenses_data:
        st.divider()
        st.subheader("📋 Expenses Log")
        df_exp = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_exp, use_container_width=True)
        st.metric("Total Deductible Expenses", f"EGP {df_exp['Cost'].sum():,.2f}")
    else:
        st.info("No expenses recorded yet.")

# ==========================
# 3. Tax & Dashboard Module
# ==========================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Financial & Tax Report")
    
    total_sales = sum(item['Amount'] for item in st.session_state.sales_data)
    total_expenses = sum(item['Cost'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses

    st.markdown("### 💰 Financial Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"EGP {total_sales:,.2f}")
    c2.metric("Total Expenses", f"EGP {total_expenses:,.2f}")
    c3.metric("Net Profit", f"EGP {net_profit:,.2f}")

    st.divider()
    st.header("⚖️ Tax Liability Analysis")
    
    tab1, tab2 = st.tabs(["🏢 Simplified Regime (Law 152)", "📝 General Regime (Law 91)"])

    with tab1:
        st.info("ℹ️ Explanation: Applies to SMEs with turnover < 10M EGP.")
        tax_152 = 0
        desc_152 = ""
        if total_sales == 0:
            st.warning("Please record sales to view tax.")
        else:
            if total_sales < 250000: tax_152, desc_152 = 1000, "Fixed Annual Fee"
            elif total_sales < 500000: tax_152, desc_152 = 2500, "Fixed Annual Fee"
            elif total_sales < 1000000: tax_152, desc_152 = 5000, "Fixed Annual Fee"
            elif total_sales < 2000000: tax_152, desc_152 = total_sales * 0.005, "0.5% of Turnover"
            elif total_sales < 3000000: tax_152, desc_152 = total_sales * 0.0075, "0.75% of Turnover"
            elif total_sales <= 10000000: tax_152, desc_152 = total_sales * 0.01, "1.0% of Turnover"
            
            if tax_152 > 0:
                st.success(f"Tax Due: EGP {tax_152:,.2f}")
                st.write(f"Calculation Basis: {desc_152}")

    with tab2:
        st.info("ℹ️ Explanation: Standard Corporate Tax (22.5% of Net Profit).")
        tax_91 = max(0, net_profit * 0.225)
        st.warning(f"Tax Due: EGP {tax_91:,.2f}")

# ==========================
# 4. Smart Tax Assistant
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    st.write("Welcome! I'm your English-speaking tax expert.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about Egyptian Tax Laws..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Answer in English as an Egyptian tax expert for SMEs: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Connection Error: {e}")

# ==========================
# 5. About Page
# ==========================
elif page == "5. About the Project":
    st.title("About SME Tax Expert")
    st.markdown("### Graduation Project - Team Members")
    
    team_data = {
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    }
    st.table(pd.DataFrame(team_data))
    st.caption("All Rights Reserved - 2026")
