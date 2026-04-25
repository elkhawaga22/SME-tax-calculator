import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة الاحترافية (SME Edition)
st.set_page_config(
    page_title="SME Tax Calculator Pro",
    layout="wide",
    page_icon="💎"
)

# --- CSS السحر لتحويل الشكل (Soft UI) ---
st.markdown("""
    <style>
    /* خلفية متدرجة ناعمة تضاهي الصورة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* تنسيق الكروت (الخانات البيضاء) */
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }

    /* تنسيق القائمة الجانبية لتكون نظيفة */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eee;
    }
    
    /* تصميم بادج البريميم بشكل "شيك" */
    .premium-badge {
        background: linear-gradient(90deg, #FFD700, #FF8C00);
        padding: 10px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    
    /* الأزرار الاحترافية */
    .stButton > button {
        background: linear-gradient(45deg, #00c6ff, #0072ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,114,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- تهيئة البيانات ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'data' not in st.session_state: 
    st.session_state.data = pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount'])

# ==========================================
# 🔐 نظام الدخول
# ==========================================
def login():
    st.markdown("<h1 style='text-align:center;'>🔐 SME Tax Calculator Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Welcome! Please log in to your specialized SME tax dashboard.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login"):
            u = st.text_input("User ID")
            p = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Dashboard")
            if submit:
                # تنظيف البيانات وتحويلها لسمول
                email, password = u.strip().lower(), p.strip()
                if email == "free_admin" and password == "free_admin": 
                    st.session_state.logged_in, st.session_state.user_role = True, "free"
                    st.rerun()
                elif email == "premium_admin" and password == "premium_admin": 
                    st.session_state.logged_in, st.session_state.user_role = True, "premium"
                    st.rerun()
                else: 
                    st.error("Invalid credentials. Try Again.")

# ==========================================
# 🚀 التطبيق الرئيسي (The Pro Dashboard)
# ==========================================
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    st.sidebar.markdown(f"#### Logged in as: **{st.session_state.user_role.upper()}**")
    
    # بادج البريميم - تصميم الصورة
    if st.session_state.user_role == "premium":
        st.sidebar.markdown('<div class="premium-badge">💎 PREMIUM ACCESS</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div style="background:#f1f5f9; padding:10px; border-radius:10px; text-align:center; color:#666; margin-bottom:20px;">STANDARD ACCOUNT</div>', unsafe_allow_html=True)
        
    menu = st.sidebar.radio("Navigation Menu", [
        "🏠 Home Dashboard", 
        "🛒 Sales & Invoicing", 
        "💸 Operating Expenses", 
        "📈 Advanced Analytics (PRO)", 
        "📂 Document Analysis (PRO)",
        "👥 Team & Legal"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.rerun()

    # --- الحسابات ---
    def calculate_taxes(revenue, expenses):
        profit = revenue - expenses
        # Law 152
        if revenue < 250000: t152 = 1000
        elif revenue < 500000: t152 = 2500
        elif revenue < 1000000: t152 = 5000
        elif revenue < 2000000: t152 = revenue * 0.005
        elif revenue < 3000000: t152 = revenue * 0.0075
        else: t152 = revenue * 0.01
        return t152, max(0, profit * 0.225)

    # ==========================================
    # 1. الصفحة الرئيسية (الشبيهة بالصورة)
    # ==========================================
    if menu == "🏠 Home Dashboard":
        st.title("SME Tax Calculator Pro")
        st.markdown("<p style='color:#666;'>Welcome! Based on Egyptian Tax Authority Standards.</p>", unsafe_allow_html=True)
        
        # كولوم للصور والملخص - نفس فكرة الصورة
        col_img, col_metrics = st.columns([1.5, 1])
        
        with col_img:
            # صورة Isometric (مثل الصورة المرفقة تماماً)
            st.image("https://img.freepik.com/free-vector/isometric-online-tax-calculator_23-2148417937.jpg?w=826&t=st=1708170284~exp=1708170884~hmac=55f52f36d4f9b8c346f041a3d9023190805c873a1104e6c9869a8b1d92636a0f", width=400)

        with col_metrics:
            rev = st.session_state.data[st.session_state.data['Type']=='Sale']['Amount'].sum()
            exp = st.session_state.data[st.session_state.data['Type']=='Expense']['Amount'].sum()
            m1, m2 = st.columns(2)
            m1.metric("Revenue", f"{rev:,.0f} ج.م")
            m2.metric("Expenses", f"{exp:,.0f} ج.م")
            m3, m4 = st.columns(2)
            profit = rev - exp
            m3.metric("Profit", f"{profit:,.0f} ج.م")
            # حاسبة الضرائب المتوقعة
            t152, t91 = calculate_taxes(rev, exp)
            m4.metric("Tax Proj.", f"{t152:,.0f} ج.م")

        st.markdown("---")
        
        # رسومات بيانية (شيك جداً ومتحركة)
        if not st.session_state.data.empty:
            st.markdown("### 📊 Quick Financial Analytics")
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # رسم بياني بار كارت للمبيعات والمصروفات
                fig_bar = px.bar(st.session_state.data, x='Category', y='Amount', color='Type', 
                                 title="Revenue vs Expenses (By Category)", barmode='group',
                                 color_discrete_sequence=['#00c6ff', '#ff4b4b'])
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with col_chart2:
                # رسم بياني دائري لتوزيع المصروفات
                exp_data = st.session_state.data[st.session_state.data['Type']=='Expense']
                if not exp_data.empty:
                    fig_pie = px.pie(exp_data, values='Amount', names='Category', 
                                 title="Operating Expenses Distribution",
                                 hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                    st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("💡 Record some transactions to see charts here!")

    # ==========================================
    # 2. المبيعات
    # ==========================================
    elif menu == "🛒 Sales & Invoicing":
        st.title("🛒 Sales Management")
        with st.form("entry_sale", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            cat = col_a.text_input("Category (e.g., Retail Sales)")
            amt = col_b.number_input("Amount (EGP)", min_value=0.0)
            if st.form_submit_button("Record Sale ✅"):
                if amt > 0:
                    new_row = {'Date': datetime.now(), 'Category': cat, 'Type': 'Sale', 'Amount': amt}
                    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("Sale Recorded!")
        if not st.session_state.data.empty:
            st.table(st.session_state.data[st.session_state.data['Type']=='Sale'][['Date', 'Category', 'Amount']])

    # ==========================================
    # 3. المصروفات
    # ==========================================
    elif menu == "💸 Operating Expenses":
        st.title("💸 Expense Management")
        with st.form("entry_exp", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            cat = col_a.text_input("Expense Item (e.g., Rent, Salaries)")
            amt = col_b.number_input("Amount (EGP)", min_value=0.0)
            if st.form_submit_button("Record Expense 💾"):
                if amt > 0:
                    new_row = {'Date': datetime.now(), 'Category': cat, 'Type': 'Expense', 'Amount': amt}
                    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("Expense Recorded!")
        if not st.session_state.data.empty:
            st.table(st.session_state.data[st.session_state.data['Type']=='Expense'][['Date', 'Category', 'Amount']])

    # ==========================================
    # 4. التحليلات المتقدمة (Premium Only)
    # ==========================================
    elif menu == "📈 Advanced Analytics (PRO)":
        st.title("🚀 Advanced Tax Planning (PRO)")
        if st.session_state.user_role == "premium":
            st.markdown("#### Tax Bracket Forecasting (Simulated)")
            # مثال للتوقع المستقبلي
            simulated_dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
            simulated_revenue = [200000, 220000, 210000, 250000, 280000, 310000, 350000, 400000, 420000, 450000, 480000, 520000]
            sim_data = pd.DataFrame({'Month': simulated_dates, 'Sales': simulated_revenue})
            
            fig = px.line(sim_data, x='Month', y='Sales', title="Projected Revenue Growth & Tax Impact")
            st.plotly_chart(fig, use_container_width=True)
            
            st.download_button("📥 Download Detailed Report", data="Report Sample Content", file_name="Report.txt")
        else:
            st.error("🚫 report download and Advanced analytics are locked. Contact admin for PREMIUM upgrade.")

    # ==========================================
    # 5. تحليل الملفات (Premium Only)
    # ==========================================
    elif menu == "📂 Document Analysis (PRO)":
        st.title("📑 Smart Document Analysis")
        if st.session_state.user_role == "premium":
            st.markdown("Upload your invoices (PDF/CSV) and the AI will analyze the legal structure.")
            st.file_uploader("Upload File")
            st.warning("⚠️ This is a simulated interface. Final AI engine integration pending.")
        else:
            st.error("🔒 Document analysis is only for Premium users.")

    # ==========================================
    # 6. فريق العمل (تم حل مشكلة الـ ID)
    # ==========================================
    elif menu == "👥 Team & Legal":
        st.title("👥 Team & Legal")
        st.markdown("Developed strictly based on Egyptian Tax Authority standards (Law 152/2020 & Law 91/2005).")
        
        team_data = {
            "Member Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
            "Student ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
        }
        st.table(pd.DataFrame(team_data))
        st.caption("Authorized Graduation Project - 2026")
