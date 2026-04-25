import streamlit as st
import pandas as pd

# 1. General Page Configuration
st.set_page_config(
    page_title="SME Tax Calculator 2026",
    layout="wide",
    page_icon="🇪🇬"
)

# --- CSS FIX: Ensuring text is visible on white metric cards ---
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #f0f2f6;
    }
    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }
    /* Force text color to be dark inside metric cards for visibility */
    [data-testid="stMetricLabel"] {
        color: #31333F !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #000000 !important;
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
    
    # Law 152 Calculation (Based on Revenue Volume)
    if revenue < 250000:
        tax_152 = 1000
        note_152 = "Fixed Tax: 1,000 EGP per year"
    elif revenue < 500000:
        tax_152 = 2500
        note_152 = "Fixed Tax: 2,500 EGP per year"
    elif revenue < 1000000:
        tax_152 = 5000
        note_152 = "Fixed Tax: 5,000 EGP per year"
    elif revenue < 2000000:
        tax_152 = revenue * 0.005
        note_152 = "0.5% of Total Revenue"
    elif revenue < 3000000:
        tax_152 = revenue * 0.0075
        note_152 = "0.75% of Total Revenue"
    else:
        tax_152 = revenue * 0.01
        note_152 = "1.0% of Total Revenue"

    # Law 91 Calculation (22.5% of Net Profit)
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
    st.info("Record all enterprise sales during the tax period.")
    
    with st.form("sales_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client Name / Invoice No.")
        amount = col2.number_input("Invoice Value (EGP)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Add Invoice ✅"):
            if amount > 0:
                st.session_state.sales_data.append({"Description": client, "Amount": amount})
                st.success("Invoice recorded successfully!")
            else:
                st.error("Please enter a valid amount.")

    if st.session_state.sales_data:
        st.markdown("### Current Sales Log")
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df_sales, use_container_width=True)
        st.metric("Total Revenue Sum", f"{df_sales['Amount'].sum():,.2f} EGP")

# ==========================================
# 2. Expenses Page
# ==========================================
elif menu == "💸 Operating Expenses":
    st.title("💸 Operating Expense Management")
    st.info("Record all administrative and general costs related to the business.")
    
    with st.form("expenses_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        item = col1.text_input("Expense Item (Rent, Salary, Utilities...)")
        cost = col2.number_input("Cost (EGP)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Record Expense 💾"):
            if cost > 0:
                st.session_state.expenses_data.append({"Item": item, "Cost": cost})
                st.success("Expense recorded successfully!")

    if st.session_state.expenses_data:
        st.markdown("### Current Expenses Log")
        df_expenses = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_expenses, use_container_width=True)
        st.metric("Total Expenses Sum", f"{df_expenses['Cost'].sum():,.2f} EGP")

# ==========================================
# 3. Reports & Tax Dashboard Page
# ==========================================
elif menu == "📊 Reports & Tax Dashboard":
    st.title("📊 Final Financial & Tax Report")
    
    total_rev = sum(d['Amount'] for d in st.session_state.sales_data)
    total_exp = sum(d['Cost'] for d in st.session_state.expenses_data)
    net_profit = total_rev - total_exp
    
    st.markdown("### Financial Performance Summary")
    # These will now have dark text on a white background
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Revenue", f"{total_rev:,.2f} EGP")
    m2.metric("Total Expenses", f"{total_exp:,.2f} EGP")
    m3.metric("Net Profit / Loss", f"{net_profit:,.2f} EGP")

    st.markdown("---")
    
    tax_152, note_152, tax_91, note_91 = calculate_taxes(total_rev, total_exp)
    
    st.markdown("### Tax Comparison (According to Egyptian Legislation)")
    t1, t2 = st.columns(2)
    
    with t1:
        st.subheader("🏢 Law 152 (Simplified)")
        st.success(f"Due Tax: {tax_152:,.2f} EGP")
        st.caption(f"Basis: {note_152}")
        
    with t2:
        st.subheader("📝 Law 91 (Income Tax)")
        st.warning(f"Due Tax: {tax_91:,.2f} EGP")
        st.caption(f"Basis: {note_91}")

    full_report = f"""
    === SME Tax Calculator Financial Report 2026 ===
    Total Revenue: {total_rev:,.2f} EGP
    Total Expenses: {total_exp:,.2f} EGP
    Net Profit: {net_profit:,.2f} EGP
    ---------------------------------------
    Tax Analysis:
    1. Law 152 (Year 2020): {tax_152:,.2f} EGP ({note_152})
    2. Law 91 (Year 2005): {tax_91:,.2f} EGP ({note_91})
    ---------------------------------------
    * This report is generated based on the Egyptian Tax Authority standards *
    """
    
    st.markdown("---")
    st.download_button(
        label="📥 Download Full Financial Report",
        data=full_report,
        file_name="Tax_Full_Report_SME.txt",
        mime="text/plain"
    )

# ==========================================
# 4. Team & Objectives Page
# ==========================================
elif menu == "👥 Team & Project Objectives":
    st.title("👥 Project Team")
    
    team_data = {
        "Full Name": [
            "Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", 
            "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", 
            "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"
        ],
        "Student ID": [
            "2202297", "2200216", "2200243", 
            "2200236", "2200190", "2202312", 
            "2200137", "2200176", "2202995"
        ]
    }
    st.table(pd.DataFrame(team_data))
    
    st.markdown("---")
    st.header("🎯 Project Objectives")
    st.markdown("""
    1. **Digital Transformation:** Contributing to Egypt's Vision 2030 by digitizing accounting processes for small businesses.
    2. **Decision Support:** Enabling business owners to compare different tax systems to choose the most suitable one.
    3. **Accounting Accuracy:** Reducing human errors in calculating complex tax brackets.
    4. **Tax Awareness:** Simplifying Egyptian tax laws (152 and 91) for everyday users.
    """)
    
    st.markdown("---")
    st.subheader("⚖️ Legal Framework")
    st.info("""
    All tax equations and benchmarks used in this system are programmed according to the latest updates from the **Egyptian Tax Authority**.
    * **Law No. 152 of 2020:** Regulating small, medium, and micro enterprises.
    * **Law No. 91 of 2005:** And its amendments regarding Income Tax.
    """)
    st.caption("Developed as a graduation project requirement for the year 2026.")
