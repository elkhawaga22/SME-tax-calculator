import streamlit as st
import pandas as pd

# 1. General Page Configuration
st.set_page_config(
    page_title="SME Tax Calculator 2026",
    layout="wide",
    page_icon="🇪🇬"
)

# --- CSS FIX: Ensuring text is visible and layout is professional ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #31333F !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    .tax-box {
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ff4b4b;
        background-color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []

# ==========================================
# Tax Calculation Engine
# ==========================================

def calculate_taxes(revenue, expenses):
    profit = revenue - expenses
    
    # Law 152 Brackets
    if revenue < 250000:
        tax_152 = 1000
        note_152 = "Fixed Tax (Revenue < 250k)"
    elif revenue < 500000:
        tax_152 = 2500
        note_152 = "Fixed Tax (Revenue 250k - 500k)"
    elif revenue < 1000000:
        tax_152 = 5000
        note_152 = "Fixed Tax (Revenue 500k - 1M)"
    elif revenue < 2000000:
        tax_152 = revenue * 0.005
        note_152 = "0.5% Rate (Revenue 1M - 2M)"
    elif revenue < 3000000:
        tax_152 = revenue * 0.0075
        note_152 = "0.75% Rate (Revenue 2M - 3M)"
    else:
        tax_152 = revenue * 0.01
        note_152 = "1.0% Rate (Revenue 3M - 10M)"

    # Law 91 (22.5% of Net Profit)
    tax_91 = max(0, profit * 0.225)
    note_91 = "22.5% of Net Commercial Profits"
    
    return tax_152, note_152, tax_91, note_91

# ==========================================
# Sidebar Navigation
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=100)
st.sidebar.title("SME Tax Calculator")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Main Menu", [
    "🛒 Sales & Invoicing",
    "💸 Operating Expenses",
    "📊 Reports & Tax Dashboard",
    "👥 Team & Project Objectives"
])

# ==========================================
# 1. Sales Page
# ==========================================
if menu == "🛒 Sales & Invoicing":
    st.title("🛒 Sales & Invoice Management")
    with st.form("sales_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client Name / Invoice No.")
        amount = col2.number_input("Invoice Value (EGP)", min_value=0.0, format="%.2f")
        if st.form_submit_button("Add Invoice ✅"):
            if amount > 0:
                st.session_state.sales_data.append({"Description": client, "Amount": amount})
                st.success("Invoice recorded!")

    if st.session_state.sales_data:
        st.markdown("### Sales Log")
        st.table(pd.DataFrame(st.session_state.sales_data))

# ==========================================
# 2. Expenses Page
# ==========================================
elif menu == "💸 Operating Expenses":
    st.title("💸 Expense Management")
    with st.form("expenses_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        item = col1.text_input("Expense Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0, format="%.2f")
        if st.form_submit_button("Record Expense 💾"):
            if cost > 0:
                st.session_state.expenses_data.append({"Item": item, "Cost": cost})
                st.success("Expense recorded!")

    if st.session_state.expenses_data:
        st.markdown("### Expenses Log")
        st.table(pd.DataFrame(st.session_state.expenses_data))

# ==========================================
# 3. Reports & Tax Dashboard (Detailed)
# ==========================================
elif menu == "📊 Reports & Tax Dashboard":
    st.title("📊 Final Tax Report & Calculation Basis")
    
    total_rev = sum(d['Amount'] for d in st.session_state.sales_data)
    total_exp = sum(d['Cost'] for d in st.session_state.expenses_data)
    net_profit = total_rev - total_exp
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Revenue", f"{total_rev:,.2f} EGP")
    m2.metric("Total Expenses", f"{total_exp:,.2f} EGP")
    m3.metric("Net Profit", f"{net_profit:,.2f} EGP")

    st.markdown("---")
    
    tax_152, note_152, tax_91, note_91 = calculate_taxes(total_rev, total_exp)
    
    tab1, tab2 = st.tabs(["🏢 Law 152 (Simplified)", "📝 Law 91 (Income Tax)"])
    
    with tab1:
        st.subheader("Law No. 152 of 2020 (SMEs)")
        st.success(f"Estimated Tax: {tax_152:,.2f} EGP")
        st.markdown(f"**Current Calculation Basis:** {note_152}")
        
        st.markdown("""
        **How Law 152 is calculated?** Tax is determined based on the total annual volume (Revenue), not profit:
        - **Revenue < 250k:** 1,000 EGP (Fixed)
        - **Revenue 250k - 500k:** 2,500 EGP (Fixed)
        - **Revenue 500k - 1M:** 5,000 EGP (Fixed)
        - **Revenue 1M - 2M:** 0.50% of Revenue
        - **Revenue 2M - 3M:** 0.75% of Revenue
        - **Revenue 3M - 10M:** 1.00% of Revenue
        """)
        
    with tab2:
        st.subheader("Law No. 91 of 2005 (Standard Tax)")
        st.warning(f"Estimated Tax: {tax_91:,.2f} EGP")
        st.markdown(f"**Current Calculation Basis:** {note_91}")
        
        st.markdown("""
        **How Law 91 is calculated?** Standard income tax is applied to the **Net Profit** (Total Revenue - Total Expenses):
        - A flat rate of **22.5%** is applied to the net annual profit.
        - Expenses must be documented and supported by official invoices to be deducted.
        """)

    st.markdown("---")
    full_report = f"Report: Revenue {total_rev:,.2f}, Law 152 Tax: {tax_152:,.2f}, Law 91 Tax: {tax_91:,.2f}"
    st.download_button("📥 Download Report", data=full_report, file_name="Report.txt")

# ==========================================
# 4. Team & Objectives
# ==========================================
elif menu == "👥 Team & Project Objectives":
    st.title("👥 Team & Objectives")
    team_data = pd.DataFrame({
        "Full Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "Student ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    })
    st.table(team_data)
    
    st.markdown("---")
    st.header("🎯 Project Objectives")
    st.markdown("""
    - **Digitalization:** Moving SME tax processes to a digital environment.
    - **Decision Support:** Comparing Laws 152 and 91 to help business owners choose the best tax treatment.
    - **Accuracy:** Implementing the official Egyptian Tax Authority brackets precisely.
    """)
    st.caption("Developed based on Egyptian Tax Authority Standards - 2026.")
