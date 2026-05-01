import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 0. Page Configuration & Custom CSS
# ==========================================
st.set_page_config(
    page_title="SME Tax Calculator Pro",
    layout="wide",
    page_icon="💎"
)

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); font-family: 'Segoe UI', sans-serif; }
    div[data-testid="stVerticalBlock"] > div {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #e2e8f0; }
    .premium-badge {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        padding: 10px; border-radius: 12px; color: white;
        text-align: center; font-weight: 700; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.3);
    }
    .stButton > button {
        background: linear-gradient(45deg, #2563eb, #1d4ed8) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600; transition: 0.3s;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37,99,235,0.3); }
    .advice-box { 
        background-color: #eff6ff; border-left: 4px solid #3b82f6; 
        padding: 15px; border-radius: 4px; margin-bottom: 10px; font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. Core Functions (المنطق البرمجي والذكاء الاصطناعي)
# ==========================================
def authenticate_user(username, password):
    u, p = username.strip().lower(), password.strip()
    if u == "free_admin" and p == "free_admin": return True, "free"
    elif u == "premium_admin" and p == "premium_admin": return True, "premium"
    return False, None

def calculate_egyptian_taxes(revenue, expenses):
    net_profit = revenue - expenses
    # Law 152 Brackets
    if revenue < 250000: tax_152 = 1000.0
    elif revenue < 500000: tax_152 = 2500.0
    elif revenue < 1000000: tax_152 = 5000.0
    elif revenue < 2000000: tax_152 = revenue * 0.005
    elif revenue < 3000000: tax_152 = revenue * 0.0075
    else: tax_152 = revenue * 0.01
    # Law 91
    tax_91 = max(0.0, net_profit * 0.225)
    return tax_152, tax_91, net_profit

def generate_tax_advice(revenue, expenses, tax_152, tax_91):
    advice = []
    if revenue == 0:
        return ["💡 سجل مبيعاتك ومصروفاتك أولاً لنتمكن من تقديم نصائح دقيقة."]
        
    if tax_152 < tax_91:
        advice.append("💡 **التحسين الضريبي:** قانون 152 (المشروعات الصغيرة) أوفر لك حالياً. يُنصح باستخراج شهادة تصنيف من جهاز تنمية المشروعات.")
    elif tax_91 < tax_152:
        advice.append("💡 **التحسين الضريبي:** قانون 91 (الدخل العام) أفضل لك بسبب ارتفاع مصروفاتك. حافظ على فواتيرك الإلكترونية لتأكيد المصروفات.")
    
    if 240000 <= revenue < 250000:
        advice.append("⚠️ **تنبيه الشريحة:** إيراداتك تقترب جداً من 250 ألف جنيه. تجاوز هذا الرقم سيرفع الضريبة المقطوعة من 1000 إلى 2500 جنيه.")
    elif 950000 <= revenue < 1000000:
        advice.append("⚠️ **تنبيه الشريحة:** أنت تقترب من حاجز المليون جنيه، حيث ستتغير الضريبة إلى نسبة مئوية (0.5%) بدلاً من مبلغ ثابت.")
        
    return advice

def generate_html_report(revenue, expenses, tax_152, tax_91, profit):
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 30px; color: #333; }}
            h1 {{ color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }}
            .summary {{ background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }}
            .tax-box {{ margin-top: 20px; padding: 15px; border-left: 5px solid #f59e0b; background: #fffbeb; }}
        </style>
    </head>
    <body>
        <h1>SME Tax Calculator - Official Report</h1>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <div class="summary">
            <h3>Financial Summary</h3>
            <p><strong>Total Revenue:</strong> {revenue:,.2f} EGP</p>
            <p><strong>Total Expenses:</strong> {expenses:,.2f} EGP</p>
            <p><strong>Net Profit:</strong> {profit:,.2f} EGP</p>
        </div>
        
        <div class="tax-box">
            <h3>Tax Liability Assessment</h3>
            <ul>
                <li><strong>Law 152 (SMEs):</strong> {tax_152:,.2f} EGP</li>
                <li><strong>Law 91 (Income Tax):</strong> {tax_91:,.2f} EGP</li>
            </ul>
        </div>
        <p><em>* This is an auto-generated preliminary assessment based on user input.</em></p>
    </body>
    </html>
    """

def add_transaction(current_df, category, trans_type, amount):
    new_record = {'Date': datetime.now().strftime("%Y-%m-%d %H:%M"), 'Category': category, 'Type': trans_type, 'Amount': amount}
    return pd.concat([current_df, pd.DataFrame([new_record])], ignore_index=True)

# ==========================================
# 2. Session State Initialization
# ==========================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'data' not in st.session_state: 
    st.session_state.data = pd.DataFrame(columns=['Date', 'Category', 'Type', 'Amount'])

# ==========================================
# 3. Login Interface
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🔐 SME Tax Calculator Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666;'>Secure access to your enterprise tax portal.</p>", unsafe_allow_html=True)
    
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        with st.form("login_form"):
            user_input = st.text_input("User ID")
            pass_input = st.text_input("Password", type="password")
            if st.form_submit_button("Access Dashboard"):
                is_valid, role = authenticate_user(user_input, pass_input)
                if is_valid:
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try Again.")

# ==========================================
# 4. Main Application (Dashboard)
# ==========================================
else:
    # Sidebar
    st.sidebar.markdown(f"#### Logged in as: **{st.session_state.user_role.upper()}**")
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

    # Calculate global metrics
    df = st.session_state.data
    total_rev = df[df['Type'] == 'Sale']['Amount'].sum() if not df.empty else 0.0
    total_exp = df[df['Type'] == 'Expense']['Amount'].sum() if not df.empty else 0.0
    t_152, t_91, profit = calculate_egyptian_taxes(total_rev, total_exp)

    # --- Home Dashboard ---
    if menu == "🏠 Home Dashboard":
        st.title("SME Financial Intelligence")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Gross Revenue", f"{total_rev:,.0f} EGP")
        m2.metric("Operating Costs", f"{total_exp:,.0f} EGP")
        m3.metric("Net Profit", f"{profit:,.0f} EGP")
        m4.metric("Est. Tax (Law 152)", f"{t_152:,.0f} EGP", delta_color="inverse")

        st.markdown("---")
        
        if not df.empty:
            st.markdown("### 📊 Quick Financial Analytics")
            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                fig_bar = px.bar(df, x='Category', y='Amount', color='Type', title="Cash Flow by Category", barmode='group', color_discrete_map={'Sale':'#00c6ff', 'Expense':'#ff4b4b'})
                st.plotly_chart(fig_bar, use_container_width=True)
            with c_chart2:
                exp_df = df[df['Type'] == 'Expense']
                if not exp_df.empty:
                    fig_pie = px.pie(exp_df, values='Amount', names='Category', title="Expenses Breakdown", hole=0.4)
                    st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("💡 Start recording sales and expenses to generate interactive charts.")

    # --- Sales Module (With Validation & Tooltips) ---
    elif menu == "🛒 Sales & Invoicing":
        st.title("🛒 Sales Ledger")
        with st.form("sale_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            cat = c1.text_input("Income Source / Client", help="أدخل اسم العميل أو نوع المبيعات.")
            amt = c2.number_input("Amount (EGP)", min_value=0.0, step=100.0, help="لا يمكن إدخال قيم سالبة.")
            
            if st.form_submit_button("Record Revenue"):
                if amt > 0 and cat.strip() != "":
                    st.session_state.data = add_transaction(st.session_state.data, cat, "Sale", amt)
                    st.success("Transaction Saved!")
                else:
                    st.error("⚠️ يرجى التأكد من كتابة الوصف وإدخال مبلغ أكبر من الصفر.")
                    
        if not df[df['Type'] == 'Sale'].empty:
            st.dataframe(df[df['Type'] == 'Sale'], use_container_width=True)

    # --- Expenses Module (With Validation & Tooltips) ---
    elif menu == "💸 Operating Expenses":
        st.title("💸 Expense Ledger")
        with st.form("exp_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            cat = c1.text_input("Expense Category", help="مثال: إيجار، رواتب، مرافق.")
            amt = c2.number_input("Amount (EGP)", min_value=0.0, step=100.0, help="سجل المصروفات المدعمة بمستندات فقط.")
            
            if st.form_submit_button("Record Cost"):
                if amt > 0 and cat.strip() != "":
                    st.session_state.data = add_transaction(st.session_state.data, cat, "Expense", amt)
                    st.success("Transaction Saved!")
                else:
                    st.error("⚠️ يرجى التأكد من كتابة الوصف وإدخال مبلغ أكبر من الصفر.")
                    
        if not df[df['Type'] == 'Expense'].empty:
            st.dataframe(df[df['Type'] == 'Expense'], use_container_width=True)

    # --- Analytics Module (PRO) - With AI Advisor & HTML Report ---
    elif menu == "📈 Advanced Analytics (PRO)":
        st.title("🚀 Advanced Analytics & AI Advisor")
        if st.session_state.user_role == "premium":
            # 1. AI Insights
            st.subheader("🧠 AI Tax Insights")
            advices = generate_tax_advice(total_rev, total_exp, t_152, t_91)
            for adv in advices:
                st.markdown(f'<div class="advice-box">{adv}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 2. Charts
            st.markdown("#### Projected Revenue Growth (Next 12 Months)")
            sim_dates = pd.date_range(start='2024-01-01', periods=12, freq='ME')
            sim_rev = [200000, 220000, 210000, 250000, 280000, 310000, 350000, 400000, 420000, 450000, 480000, 520000]
            fig = px.line(x=sim_dates, y=sim_rev, markers=True, title="Simulated AI Revenue Prediction")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 3. HTML Report Download
            st.subheader("📑 Generate Official Report")
            html_content = generate_html_report(total_rev, total_exp, t_152, t_91, profit)
            st.download_button(
                label="📥 Download Detailed Report (HTML for PDF Print)",
                data=html_content,
                file_name=f"SME_Tax_Report_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
        else:
            st.error("🚫 Forecasting, AI Advisor, and Report Downloads are PREMIUM features. Please upgrade.")

    # --- Document Analysis (PRO) ---
    elif menu == "📂 Document Analysis (PRO)":
        st.title("📑 Smart Document Parsing")
        if st.session_state.user_role == "premium":
            st.write("Upload PDF or CSV invoices to automatically extract financial data.")
            st.file_uploader("Drop your files here")
            st.warning("⚠️ Module under construction: OCR Engine initialization pending.")
        else:
            st.error("🔒 Document Analysis is restricted to Premium Users.")

    # --- Team Module ---
    elif menu == "👥 Team & Legal":
        st.title("👥 Project Developers")
        team_data = {
            "Member Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
            "Student ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
        }
        st.table(pd.DataFrame(team_data))
        st.markdown("---")
        st.info("Developed strictly based on **Egyptian Tax Authority Standards (Law 152/2020 & Law 91/2005)** for Graduation Project 2026.")
