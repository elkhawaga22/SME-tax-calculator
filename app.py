import streamlit as st
import pandas as pd
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# --- تهيئة مخزن البيانات (Session State) ---
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.title("🏢 SME Tax Expert")
st.sidebar.markdown("**Graduation Project 2026**") 

page = st.sidebar.radio("Navigation", [
    "🏠 Project Overview",
    "🛒 Sales & Invoicing", 
    "💸 Operating Expenses", 
    "📊 Tax Dashboard & Report",
    "👥 About the Team"
])

# ==========================================
# 0. Project Overview & Goals
# ==========================================
if page == "🏠 Project Overview":
    st.title("🇪🇬 Digital Transformation in Egyptian Taxation")
    st.subheader("Project Objectives")
    st.markdown("""
    * **Automation:** Simplifying complex tax calculations for Small and Medium Enterprises (SMEs).
    * **Accuracy:** Reducing human error in determining tax brackets according to Egyptian law.
    * **Awareness:** Helping business owners understand the difference between Law 152 and Law 91.
    * **Digitalization:** Aligning with Egypt's Vision 2030 for digital financial services.
    """)
    
    st.warning("""
    ⚠️ **Legal Disclaimer:** All calculations provided by this application are based on the **Egyptian Tax Law No. 152 of 2020** (for SMEs) and **Law No. 91 of 2005** (Income Tax). Please consult a certified public accountant for official filing.
    """)

# ==========================================
# 1. Sales Module
# ==========================================
elif page == "🛒 Sales & Invoicing":
    st.title("🛒 Sales Management")
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Save Invoice") and amount > 0:
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("Invoice saved successfully! ✅")
    
    if st.session_state.sales_data:
        st.dataframe(pd.DataFrame(st.session_state.sales_data), use_container_width=True)

# ==========================================
# 2. Expenses Module
# ==========================================
elif page == "💸 Operating Expenses":
    st.title("💸 Expense Management")
    with st.form("add_exp"):
        col1, col2 = st.columns(2)
        item = col1.text_input("Expense Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Record Expense") and cost > 0:
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("Expense recorded! ✅")
    
    if st.session_state.expenses_data:
        st.dataframe(pd.DataFrame(st.session_state.expenses_data), use_container_width=True)

# ==========================================
# 3. Tax Dashboard & Export Report
# ==========================================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Financial Summary & Tax Report")
    
    total_sales = sum(item['Amount'] for item in st.session_state.sales_data)
    total_expenses = sum(item['Cost'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses
    
    # حساب الضريبة (قانون 152)
    if total_sales < 250000: tax_152 = 1000
    elif total_sales < 500000: tax_152 = 2500
    elif total_sales < 1000000: tax_152 = 5000
    elif total_sales < 2000000: tax_152 = total_sales * 0.005
    elif total_sales < 3000000: tax_152 = total_sales * 0.0075
    else: tax_152 = total_sales * 0.01

    # حساب الضريبة (قانون 91)
    tax_91 = max(0, net_profit * 0.225)

    # عرض النتائج
    c1, c2, c3 = st.columns(3)
    c1.metric("Revenue", f"{total_sales:,.2f} EGP")
    c2.metric("Expenses", f"{total_expenses:,.2f} EGP")
    c3.metric("Net Profit", f"{net_profit:,.2f} EGP")

    st.markdown("---")
    
    # خيار تحميل التقرير
    report_text = f"""
    SME TAX EXPERT REPORT - 2026
    ----------------------------
    Total Revenue: {total_sales:,.2f} EGP
    Total Expenses: {total_expenses:,.2f} EGP
    Net Profit: {net_profit:,.2f} EGP
    
    TAX CALCULATIONS (Based on Egyptian Law):
    1. Law 152 (Simplified): {tax_152:,.2f} EGP
    2. Law 91 (Standard 22.5%): {tax_91:,.2f} EGP
    
    *Disclaimer: This is a preliminary report based on provided data.*
    """
    
    st.download_button(
        label="📥 Download Full Financial Report",
        data=report_text,
        file_name="Tax_Report.txt",
        mime="text/plain"
    )

    tab1, tab2 = st.tabs(["🏢 Law 152 Analysis", "📝 Law 91 Analysis"])
    with tab1:
        st.success(f"Estimated Tax: EGP {tax_152:,.2f}")
        st.write("**Note:** Under Law 152, tax is calculated on total volume, which is ideal for SMEs with high expenses.")
    with tab2:
        st.warning(f"Estimated Tax: EGP {tax_91:,.2f}")
        st.write("**Note:** Under Law 91, tax is 22.5% of net profit after deducting all documented expenses.")

# ==========================================
# 4. About Page
# ==========================================
elif page == "👥 About the Team":
    st.title("Project Team")
    team_data = {
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    }
    st.table(pd.DataFrame(team_data))
