import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة المتقدمة
st.set_page_config(
    page_title="SME Tax Calculator Pro",
    layout="wide",
    page_icon="💎"
)

# --- CSS التنسيق "الشيك" جداً ---
def apply_custom_style(role):
    primary_color = "#D4AF37" if role == "premium" else "#1E3A8A" # ذهبي للبريميم / أزرق للمجاني
    
    st.markdown(f"""
        <style>
        /* الخلفية العامة */
        .stApp {{
            background-color: #f4f7f9;
        }}
        
        /* تنسيق الكروت (Metrics) */
        [data-testid="stMetric"] {{
            background: white !important;
            padding: 25px !important;
            border-radius: 15px !important;
            border-top: 5px solid {primary_color} !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
        }}
        
        /* تنسيق القائمة الجانبية */
        section[data-testid="stSidebar"] {{
            background-color: #ffffff !important;
            border-right: 1px solid #e0e0e0;
        }}
        
        /* بادج البريميم */
        .premium-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            background: linear-gradient(45deg, #D4AF37, #F9E79F);
            color: #000;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(212, 175, 55, 0.3);
        }}
        
        /* العناوين */
        h1, h2, h3 {{
            color: #1a202c !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- تهيئة البيانات ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []

# ==========================================
# واجهة الدخول (Login)
# ==========================================
def login():
    st.markdown("<h1 style='text-align: center;'>🔐 SME Tax Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Log in to manage your taxes professionally</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("---")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.button("Access Dashboard", use_container_width=True)
            
            if submit:
                u, p = email.strip().lower(), password.strip()
                if u == "free_admin" and p == "free_admin":
                    st.session_state.logged_in, st.session_state.user_role = True, "free"
                    st.rerun()
                elif u == "premium_admin" and p == "premium_admin":
                    st.session_state.logged_in, st.session_state.user_role = True, "premium"
                    st.rerun()
                else:
                    st.error("Wrong credentials. Please try again.")

# ==========================================
# التطبيق الرئيسي
# ==========================================
if not st.session_state.logged_in:
    login()
else:
    apply_custom_style(st.session_state.user_role)
    
    # Sidebar
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
    
    if st.session_state.user_role == "premium":
        st.sidebar.markdown('<div class="premium-badge">💎 PREMIUM ACCOUNT</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div style="text-align:center; color:#666; margin-bottom:20px;">STANDARD ACCOUNT</div>', unsafe_allow_html=True)

    # تم تبسيط الأسماء لضمان ظهورها
    menu_options = {
        "Sales": "🛒 Sales & Invoicing",
        "Expenses": "💸 Operating Expenses",
        "Reports": "📊 Tax Dashboard",
        "Team": "👥 Team & Objectives"
    }
    
    choice = st.sidebar.radio("Main Menu", list(menu_options.values()))
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Log Out 🚪", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # --- الحسابات ---
    def get_tax_report(rev, exp):
        profit = rev - exp
        # القانون 152
        if rev < 250000: t152 = 1000
        elif rev < 500000: t152 = 2500
        elif rev < 1000000: t152 = 5000
        elif rev < 2000000: t152 = rev * 0.005
        elif rev < 3000000: t152 = rev * 0.0075
        else: t152 = rev * 0.01
        return t152, max(0, profit * 0.225)

    # --- الصفحات ---
    if choice == menu_options["Sales"]:
        st.title("🛒 Sales Management")
        with st.container():
            c1, c2 = st.columns(2)
            client = c1.text_input("Client")
            amount = c2.number_input("Amount (EGP)", min_value=0.0)
            if st.button("Add Record ✅", use_container_width=True):
                if amount > 0: st.session_state.sales_data.append({"Client": client, "Amount": amount})
        
        if st.session_state.sales_data:
            st.table(pd.DataFrame(st.session_state.sales_data))

    elif choice == menu_options["Expenses"]:
        st.title("💸 Expenses Management")
        with st.container():
            item = st.text_input("Expense Item")
            cost = st.number_input("Cost (EGP)", min_value=0.0)
            if st.button("Record Expense 💾", use_container_width=True):
                if cost > 0: st.session_state.expenses_data.append({"Item": item, "Cost": cost})
        
        if st.session_state.expenses_data:
            st.table(pd.DataFrame(st.session_state.expenses_data))

    elif choice == menu_options["Reports"]:
        st.title("📊 Financial Intelligence Dashboard")
        rev = sum(d['Amount'] for d in st.session_state.sales_data)
        exp = sum(d['Cost'] for d in st.session_state.expenses_data)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Revenue", f"{rev:,.2f} EGP")
        m2.metric("Expenses", f"{exp:,.2f} EGP")
        m3.metric("Net Profit", f"{rev - exp:,.2f} EGP")

        st.markdown("### Estimated Taxes")
        t152, t91 = get_chat_response = get_tax_report(rev, exp)
        
        c_a, c_b = st.columns(2)
        c_a.success(f"Law 152: {t152:,.2f} EGP")
        c_b.warning(f"Law 91: {t91:,.2f} EGP")

        st.markdown("---")
        if st.session_state.user_role == "premium":
            st.info("💎 Premium Feature: You can download the full PDF/Text report.")
            st.download_button("📥 Download Official Report", data=f"Revenue: {rev}, Profit: {rev-exp}", file_name="Report.txt")
        else:
            st.error("🚫 Report download is locked for Free accounts. Contact admin for Premium.")

    # هذه هي الصفحة التي كانت تختفي، تم التأكد من ربطها بالقاموس (Dictionary)
    elif choice == menu_options["Team"]:
        st.title("👥 Team & Objectives")
        
        st.subheader("Project Mission")
        st.markdown("""
        Digitizing the Egyptian tax system for SMEs to align with **Egypt Vision 2030**.
        Our tool ensures accuracy, legality, and ease of use.
        """)
        
        st.subheader("Our Team")
        team = pd.DataFrame({
            "Member Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
            "Student ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
        })
        st.table(team)
        
        st.info("⚠️ All calculations are strictly based on the Egyptian Tax Authority standards (Law 152/2020 & 91/2005).")
