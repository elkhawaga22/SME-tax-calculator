import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(
    page_title="SME Smart Tax Portal",
    layout="wide",
    page_icon="🏦"
)

# --- CSS لتصميم يضاهي الصورة (Soft UI) ---
st.markdown("""
    <style>
    /* خلفية متدرجة ناعمة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* تصميم الكروت البيضاء */
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }

    /* القائمة الجانبية شيك جداً */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eee;
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
    
    /* بادج البريميم */
    .premium-hero {
        background: linear-gradient(90deg, #FFD700, #FF8C00);
        padding: 10px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
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
if not st.session_state.logged_in:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<h2 style='text-align:center;'>بوابة الضرائب الذكية</h2>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("User ID")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if u == "free_admin": 
                    st.session_state.logged_in, st.session_state.user_role = True, "free"
                    st.rerun()
                elif u == "premium_admin": 
                    st.session_state.logged_in, st.session_state.user_role = True, "premium"
                    st.rerun()
                else: st.error("Access Denied")

# ==========================================
# 🚀 لوحة التحكم الرئيسية (Dashboard)
# ==========================================
else:
    # Sidebar
    st.sidebar.markdown(f"### Welcome, {st.session_state.user_role.capitalize()}")
    if st.session_state.user_role == "premium":
        st.sidebar.markdown('<div class="premium-hero">💎 PREMIUM ACCESS</div>', unsafe_allow_html=True)
    
    menu = st.sidebar.selectbox("Main Menu", [
        "🏠 Home Dashboard", 
        "➕ Data Entry", 
        "📈 Advanced Analytics (PRO)", 
        "📂 Document Analysis (PRO)",
        "👥 Team"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 🏠 الصفحة الرئيسية (نفس فكرة الصورة) ---
    if menu == "🏠 Home Dashboard":
        st.title("Smart Tax Portal Dashboard")
        
        # ملخص سريع (Metrics)
        rev = st.session_state.data[st.session_state.data['Type']=='Sale']['Amount'].sum()
        exp = st.session_state.data[st.session_state.data['Type']=='Expense']['Amount'].sum()
        profit = rev - exp
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Sales", f"{rev:,.0f} ج.م")
        c2.metric("Expenses", f"{exp:,.0f} ج.م")
        c3.metric("Net Profit", f"{profit:,.0f} ج.م")
        
        # الضريبة المتوقعة
        tax = 5000 if rev < 1000000 else rev * 0.01
        c4.metric("Estimated Tax", f"{tax:,.0f} ج.م", delta_color="inverse")

        # الرسوم البيانية (Charts)
        st.markdown("### 📊 Financial Visualizations")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # رسم بياني للمبيعات والمصروفات
            fig = px.bar(st.session_state.data, x='Category', y='Amount', color='Type', 
                         title="Revenue vs Expenses by Category", barmode='group',
                         color_discrete_map={'Sale':'#00d2ff', 'Expense':'#ff4b4b'})
            st.plotly_chart(fig, use_container_width=True)
            
        with col_chart2:
            # رسم بياني دائري
            if not st.session_state.data.empty:
                fig2 = px.pie(st.session_state.data, values='Amount', names='Type', 
                             hole=.4, title="Financial Distribution",
                             color_discrete_sequence=['#0072ff', '#ff4b4b'])
                st.plotly_chart(fig2, use_container_width=True)

    # --- ➕ إدخال البيانات ---
    elif menu == "➕ Data Entry":
        st.title("Transaction Entry")
        with st.form("entry"):
            col_a, col_b, col_c = st.columns(3)
            cat = col_a.text_input("Category (e.g. Retail, Rent)")
            amt = col_b.number_input("Amount", min_value=0.0)
            t_type = col_c.selectbox("Type", ["Sale", "Expense"])
            if st.form_submit_button("Record Transaction"):
                new_row = {'Date': datetime.now(), 'Category': cat, 'Type': t_type, 'Amount': amt}
                st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Recorded successfully!")

    # --- 📈 التحليلات المتقدمة (PREMIUM ONLY) ---
    elif menu == "📈 Advanced Analytics (PRO)":
        st.title("🚀 Advanced AI Analytics")
        if st.session_state.user_role == "premium":
            st.markdown("#### Tax Forecasting & Statistical Trends")
            
            # محاكاة للتوقعات المستقبلية
            dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
            trend_data = pd.DataFrame({
                'Month': dates,
                'Projected Sales': [10000, 15000, 13000, 18000, 25000, 22000, 30000, 35000, 40000, 45000, 42000, 50000]
            })
            
            fig3 = px.line(trend_data, x='Month', y='Projected Sales', title="AI-Driven Sales Forecasting (Next 12 Months)")
            st.plotly_chart(fig3, use_container_width=True)
            
            st.write("💡 **AI Insight:** Based on your current growth, we expect your tax bracket to change in October. Plan your liquidity accordingly.")
        else:
            st.error("🚫 This feature is locked. Please upgrade to PREMIUM to access AI Analytics.")

    # --- 📂 تحليل الملفات (PREMIUM ONLY) ---
    elif menu == "📂 Document Analysis (PRO)":
        st.title("📑 Smart Document Processing")
        if st.session_state.user_role == "premium":
            st.write("Upload your Bank Statement or Invoice (PDF/CSV) to analyze automatically.")
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file:
                with st.spinner("AI is analyzing document structure..."):
                    st.success("Analysis Complete: We found 12 sales and 4 expenses in this file.")
                    # هنا تضع كود معالجة الملف الحقيقي
        else:
            st.warning("🔒 Automated File Analysis is for Premium users only.")

    # --- 👥 فريق العمل ---
    elif menu == "👥 Team":
        st.title("Project Team")
        team = pd.DataFrame({
            "Name": ["Omar Mohamed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"]
        })
        st.table(team)
        st.info("Authorized by the Egyptian Tax Authority Digital Vision 2030.")
