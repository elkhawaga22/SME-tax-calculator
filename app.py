import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# --- تهيئة مخزن البيانات ---
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []

# --- القائمة الجانبية ---
st.sidebar.title("🏢 SME Tax Expert")
st.sidebar.markdown("**Graduation Project 2026**") 

page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", 
    "2. Operating Expenses", 
    "3. Tax Dashboard & Report",
    "4. About the Project"
])

# ==========================
# 1. Sales Module
# ==========================
if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management")
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Save Invoice") and amount > 0:
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("Invoice saved! ✅")
    
    if st.session_state.sales_data:
        st.dataframe(pd.DataFrame(st.session_state.sales_data), use_container_width=True)

# ==========================
# 2. Expenses Module
# ==========================
elif page == "2. Operating Expenses":
    st.title("💸 Expense Management")
    with st.form("add_exp"):
        col1, col2 = st.columns(2)
        item = col1.text_input("Expense Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Record Expense") and cost > 0:
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("Recorded! ✅")
    
    if st.session_state.expenses_data:
        st.dataframe(pd.DataFrame(st.session_state.expenses_data), use_container_width=True)

# ==========================
# 3. Tax Dashboard & Report (المعادلات والتفاصيل هنا)
# ==========================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Detailed Financial & Tax Report")
    
    total_sales = sum(item['Amount'] for item in st.session_state.sales_data)
    total_expenses = sum(item['Cost'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses
    
    # ملخص سريع
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"{total_sales:,.2f}")
    c2.metric("Total Expenses", f"{total_expenses:,.2f}")
    c3.metric("Net Profit", f"{net_profit:,.2f}")

    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🏢 Law 152 (Simplified)", "📝 Law 91 (Standard)"])
    
    with tab1:
        st.subheader("Law 152 for Small Enterprises")
        st.write("This law calculates tax based on **Total Revenue** (Sales) regardless of expenses.")
        
        # منطق حساب قانون 152 بالتفصيل
        if total_sales < 250000:
            tax_152 = 1000
            calc_note = "Fixed tax: 1,000 EGP (Revenue < 250k)"
        elif total_sales < 500000:
            tax_152 = 2500
            calc_note = "Fixed tax: 2,500 EGP (Revenue 250k - 500k)"
        elif total_sales < 1000000:
            tax_152 = 5000
            calc_note = "Fixed tax: 5,000 EGP (Revenue 500k - 1M)"
        elif total_sales < 2000000:
            tax_152 = total_sales * 0.005
            calc_note = "Rate: 0.5% of total revenue"
        elif total_sales < 3000000:
            tax_152 = total_sales * 0.0075
            calc_note = "Rate: 0.75% of total revenue"
        else:
            tax_152 = total_sales * 0.01
            calc_note = "Rate: 1.0% of total revenue"

        st.success(f"**Estimated Tax: EGP {tax_152:,.2f}**")
        st.info(f"**Calculation Basis:** {calc_note}")
        
    with tab2:
        st.subheader("Law 91 (Income Tax)")
        st.write("This tax is calculated based on **Net Profit** (Revenue - Expenses).")
        
        # منطق حساب قانون 91 (ضريبة الأرباح التجارية)
        tax_91_rate = 0.225
        tax_91 = max(0, net_profit * tax_91_rate)
        
        st.warning(f"**Estimated Tax: EGP {tax_91:,.2f}**")
        st.info(f"**Calculation Basis:** 22.5% of Net Profit ({net_profit:,.2f} x 22.5%)")
        
        if net_profit <= 0:
            st.error("Note: No tax due because there is no net profit.")

# ==========================
# 4. About Page
# ==========================
elif page == "4. About the Project":
    st.title("Project Team")
    team_data = {
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    }
    st.table(pd.DataFrame(team_data))
