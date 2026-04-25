import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="SME Tax Calculator 2026",
    layout="wide",
    page_icon="🔐"
)

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'sales_data' not in st.session_state: 
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: 
    st.session_state.expenses_data = []

# --- CSS Styling ---
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #31333F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# AUTHENTICATION INTERFACE
# ==========================================
def login():
    st.title("🔐 SME Tax Calculator - Login")
    st.info("Welcome back! Please enter your credentials to access the system.")
    
    with st.form("login_form"):
        email = st.text_input("Email / Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if email == "free_admin" and password == "free_admin":
                st.session_state.logged_in = True
                st.session_state.user_role = "free"
                st.rerun()
            elif email == "premium_admin" and password == "premium_admin":
                st.session_state.logged_in = True
                st.session_state.user_role = "premium"
                st.rerun()
            else:
                st.error("Invalid email or password. Please try again.")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================
if not st.session_state.logged_in:
    login()
else:
    # Sidebar Navigation
    st.sidebar.title("SME Tax Calculator")
    st.sidebar.write(f"Logged in as: **{st.session_state.user_role.upper()}**")
    
    menu = st.sidebar.radio("Navigation", [
        "🛒 Sales & Invoicing",
        "💸 Operating Expenses",
        "📊 Reports & Tax Dashboard",
        "👥 Team & Objectives"
    ])
    
    if st.sidebar.button("Logout 🚪"):
        logout()

    # --- Tax Engine ---
    def calculate_taxes(rev, exp):
        profit = rev - exp
        if rev < 250000: tax_152 = 1000
        elif rev < 500000: tax_152 = 2500
        elif rev < 1000000: tax_152 = 5000
        elif rev < 2000000: tax_152 = rev * 0.005
        elif rev < 3000000: tax_152 = rev * 0.0075
        else: tax_152 = rev * 0.01
        
        tax_91 = max(0, profit * 0.225)
        return tax_152, tax_91

    # --- 1. Sales ---
    if menu == "🛒 Sales & Invoicing":
        st.title("🛒 Sales Management")
        with st.form("sales_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            client = col1.text_input("Client")
            amount = col2.number_input("Amount (EGP)", min_value=0.0)
            if st.form_submit_button("Add ✅"):
                if amount > 0: st.session_state.sales_data.append({"Description": client, "Amount": amount})

        if st.session_state.sales_data:
            st.table(pd.DataFrame(st.session_state.sales_data))

    # --- 2. Expenses ---
    elif menu == "💸 Operating Expenses":
        st.title("💸 Expense Management")
        with st.form("exp_form", clear_on_submit=True):
            item = st.text_input("Expense Item")
            cost = st.number_input("Cost (EGP)", min_value=0.0)
            if st.form_submit_button("Save 💾"):
                if cost > 0: st.session_state.expenses_data.append({"Item": item, "Cost": cost})

        if st.session_state.expenses_data:
            st.table(pd.DataFrame(st.session_state.expenses_data))

    # --- 3. Dashboard (The Download Restriction Happens Here) ---
    elif menu == "📊 Reports & Tax Dashboard":
        st.title("📊 Financial Report")
        rev = sum(d['Amount'] for d in st.session_state.sales_data)
        exp = sum(d['Cost'] for d in st.session_state.expenses_data)
        profit = rev - exp
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"{rev:,.2f} EGP")
        m2.metric("Total Expenses", f"{exp:,.2f} EGP")
        m3.metric("Net Profit", f"{profit:,.2f} EGP")

        tax_152, tax_91 = calculate_taxes(rev, exp)
        
        col_a, col_b = st.columns(2)
        with col_a: st.success(f"Law 152 Tax: {tax_152:,.2f} EGP")
        with col_b: st.warning(f"Law 91 Tax: {tax_91:,.2f} EGP")

        st.markdown("---")
        
        # --- ACCESS CONTROL ---
        if st.session_state.user_role == "premium":
            report_txt = f"Report: Revenue {rev}, Tax 152: {tax_152}, Tax 91: {tax_91}"
            st.download_button("📥 Download Official Report", data=report_txt, file_name="Tax_Report.txt")
        else:
            st.error("🚫 Report download is disabled for FREE accounts. Upgrade to PREMIUM to download.")

    # --- 4. Team & Objectives ---
    elif menu == "👥 Team & Project Objectives":
        st.title("👥 Team & Objectives")
        team = pd.DataFrame({
            "Full Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
            "Student ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
        })
        st.table(team)
        st.markdown("---")
        st.info("This system is programmed according to the Egyptian Tax Authority standards (Law 152/2020 & Law 91/2005).")
