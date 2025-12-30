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
    
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client_name = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0, step=100.0)
        submit_sale = st.form_submit_button("Save Invoice")
        
        if submit_sale and amount > 0:
            st.session_state.sales_data.append({"Client": client_name, "Amount": amount})
            st.success("Invoice saved successfully! ✅")

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
    
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        desc = col1.text_input("Expense Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0, step=100.0)
        submit_exp = st.form_submit_button("Record Expense")
        
        if submit_exp and cost > 0:
            st.session_state.expenses_data.append({"Item": desc, "Cost": cost})
            st.success("Expense recorded successfully! ✅")

    if st.session_state.expenses_data:
        st.subheader("Expenses Log")
        df_exp = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_exp, use_container_width=True)
        st.metric("Total Expenses", f"EGP {df_exp['Cost'].sum():,.2f}")
    else:
        st.info("No expenses recorded yet.")

# ==========================
# 3. Tax & Dashboard Module
# ==========================
elif page == "3. Financial Position & Tax":
    st.header("📊 Financial & Tax Dashboard")

    total_sales = sum(item['Amount'] for item in st.session_state.sales_data)
    total_expenses = sum(item['Cost'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"EGP {total_sales:,.2f}")
    col2.metric("Total Expenses", f"EGP {total_expenses:,.2f}")
    col3.metric("Net Profit", f"EGP {net_profit:,.2f}", delta_color="normal")

    st.markdown("---")
    st.subheader("⚖️ Tax Calculation Engine")

    # 1. Simplified Regime (Law 152/2020)
    st.markdown("#### 1️⃣ Simplified Regime (Law 152/2020)")
    tax_152 = 0
    desc_152 = ""
    
    if total_sales == 0:
        st.warning("Please record sales to calculate taxes.")
    else:
        if total_sales < 250000: tax_152, desc_152 = 1000, "Fixed Amount"
        elif total_sales < 500000: tax_152, desc_152 = 2500, "Fixed Amount"
        elif total_sales < 1000000: tax_152, desc_152 = 5000, "Fixed Amount"
        elif total_sales < 2000000: tax_152, desc_152 = total_sales * 0.005, "Rate 0.50%"
        elif total_sales < 3000000: tax_152, desc_152 = total_sales * 0.0075, "Rate 0.75%"
        elif total_sales <= 10000000: tax_152, desc_152 = total_sales * 0.01, "Rate 1.00%"
        
        if tax_152 > 0:
            st.success(f"Tax Liability (Simplified): EGP {tax_152:,.2f} ({desc_152})")
        else:
            st.error("Not Applicable (Turnover > 10M EGP)")

    # 2. General Regime (Law 91/2005)
    st.markdown("#### 2️⃣ General Regime (Law 91/2005)")
    tax_91 = max(0, net_profit * 0.225)
    st.info(f"Tax Liability (General): EGP {tax_91:,.2f} (22.5% on Net Profit)")

    # Recommendation
    if total_sales > 0:
        st.markdown("### 💡 AI Recommendation")
        if tax_152 > 0 and tax_152 < tax_91:
            st.write(f"We recommend the **Simplified Regime** to save **EGP {tax_91 - tax_152:,.2f}**.")
        elif tax_91 < tax_152:
            st.write("The **General Regime** might be more beneficial due to high expenses.")