import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="SME Tax Calculator Pro",
    layout="wide",
    page_icon="🏦"
)

# --- CSS السحر لتغيير الشكل 180 درجة ---
st.markdown("""
    <style>
    /* تثبيت الخلفية لتكون احترافية */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* تنسيق القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* تنسيق الكروت (الخانات البيضاء) */
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    
    /* ستايل مخصص للكروت البيضاء */
    .css-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
        border: 1px solid #f1f5f9;
    }

    /* ستايل المبيعات والمصروفات */
    [data-testid="stMetric"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* تنسيق بادج البريميم بشكل "شيك" */
    .premium-tag {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.75rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 0.8rem;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    /* تعديل الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 0.75rem;
        height: 3rem;
        background-color: #1e293b !important;
        color: white !important;
        font-weight: 600;
        border: none !important;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #334155 !important;
        transform: translateY(-2px);
    }

    /* إخفاء العلامات غير المرغوبة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- تهيئة البيانات ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'sales' not in st.session_state: st.session_state.sales = []
if 'expenses' not in st.session_state: st.session_state.expenses = []

# ==========================================
# 🔐 واجهة تسجيل الدخول (Clean Login)
# ==========================================
if not st.session_state.logged_in:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center;'>
                <h1 style='color: #1e293b; font-size: 2.5rem;'>SME Tax Expert</h1>
                <p style='color: #64748b;'>The most trusted tax calculator in Egypt</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login"):
            email = st.text_input("Username").strip().lower()
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In"):
                if email == "free_admin" and password == "free_admin":
                    st.session_state.logged_in, st.session_state.user_role = True, "free"
                    st.rerun()
                elif email == "premium_admin" and password == "premium_admin":
                    st.session_state.logged_in, st.session_state.user_role = True, "premium"
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ==========================================
# 🚀 التطبيق الرئيسي (The Dashboard)
# ==========================================
else:
    # Sidebar
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=70)
    
    if st.session_state.user_role == "premium":
        st.sidebar.markdown('<div class="premium-tag">💎 PREMIUM USER</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div style="background:#f1f5f9; padding:10px; border-radius:10px; text-align:center; font-size:12px; font-weight:bold; color:#64748b; margin-bottom:20px;">STANDARD ACCOUNT</div>', unsafe_allow_html=True)

    choice = st.sidebar.radio("MAIN NAVIGATION", [
        "📊 Dashboard Home",
        "🛒 Sales Management",
        "💸 Expense Tracking",
        "👥 Team & Legal"
    ])
    
    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Log Out 🚪"):
        st.session_state.logged_in = False
        st.rerun()

    # --- صفحات التطبيق ---
    if choice == "🛒 Sales Management":
        st.title("🛒 Sales Management")
        st.markdown("<p style='color:#64748b'>Record and track your business invoices.</p>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([2, 1])
            client = col1.text_input("Client/Invoice Detail")
            amt = col2.number_input("Amount (EGP)", min_value=0.0)
            if st.button("Add Record to Ledger"):
                if amt > 0: 
                    st.session_state.sales.append({"Client": client, "Amount": amt})
                    st.success("Invoice added!")
        
        if st.session_state.sales:
            st.markdown("### Transaction History")
            st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

    elif choice == "💸 Expense Tracking":
        st.title("💸 Expense Management")
        with st.form("exp"):
            it = st.text_input("Expense Description")
            ct = st.number_input("Cost (EGP)", min_value=0.0)
            if st.form_submit_button("Record Expense"):
                if ct > 0: st.session_state.expenses.append({"Item": it, "Cost": ct})
        
        if st.session_state.expenses:
            st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

    elif choice == "📊 Dashboard Home":
        st.title("📊 Financial Intelligence")
        
        rev = sum(d['Amount'] for d in st.session_state.sales)
        exp = sum(d['Cost'] for d in st.session_state.expenses)
        profit = rev - exp
        
        # Metrics Row
        c1, c2, c3 = st.columns(3)
        c1.metric("Gross Revenue", f"{rev:,.0f} EGP")
        c2.metric("Operating Costs", f"{exp:,.0f} EGP")
        c3.metric("Net Profit", f"{profit:,.0f} EGP", delta=f"{profit:,.0f}")

        st.markdown("---")
        st.subheader("Tax Projections")
        
        # Tax Logic
        t152 = 1000 if rev < 250000 else 2500 if rev < 500000 else 5000 if rev < 1000000 else rev*0.01
        t91 = max(0, profit * 0.225)
        
        tx1, tx2 = st.columns(2)
        with tx1:
            st.info(f"**Law 152 (SMEs)**\n\nEstimated Tax: **{t152:,.2f} EGP**")
        with tx2:
            st.warning(f"**Law 91 (Income Tax)**\n\nEstimated Tax: **{t91:,.2f} EGP**")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.user_role == "premium":
            st.download_button("📥 Generate Official PDF Report", data="Report Content", file_name="SME_Tax_Report.txt")
        else:
            st.error("🔒 The 'Official Report Download' is a Premium Feature. Please upgrade to unlock.")

    elif choice == "👥 Team & Legal":
        st.title("👥 Project Information")
        
        st.markdown("### Team Members")
        team = pd.DataFrame({
            "Full Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
            "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
        })
        st.table(team)
        
        st.markdown("---")
        st.markdown("""
        **Project Objectives:** Digitalizing tax awareness for SMEs in Egypt, facilitating accurate calculation according to **Law 152/2020** and **Law 91/2005**.
        """)
