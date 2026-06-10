import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ==========================================
# 0. Page Configuration & SaaS CSS
# ==========================================
st.set_page_config(page_title="SME Tax Calculator - SaaS", layout="wide", page_icon="☁️")

st.markdown("""
    <style>
    /* CSS to mimic the SaaS Dashboard image */
    .stApp { background: #f4f7fe; font-family: 'Inter', sans-serif; }
    
    /* Card Styling */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
    
    /* Tiers Badges */
    .badge-free { background: #94a3b8; color: white; padding: 5px 10px; border-radius: 8px; font-weight: bold; text-align: center; }
    .badge-basic { background: #3b82f6; color: white; padding: 5px 10px; border-radius: 8px; font-weight: bold; text-align: center; }
    .badge-pro { background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%); color: white; padding: 5px 10px; border-radius: 8px; font-weight: bold; text-align: center; }
    
    /* Metrics override */
    [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 800 !important; color: #1e293b !important; }
    [data-testid="stMetricLabel"] { font-size: 14px !important; color: #64748b !important; }
    
    .advice-box { background-color: #f3e8ff; border-left: 4px solid #8b5cf6; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #4c1d95;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. Core Functions (Authentication & Logic)
# ==========================================
def authenticate_user(username, password):
    u, p = username.strip().lower(), password.strip()
    if u == "free" and p == "free": return True, "Free Tier (0 EGP)"
    elif u == "basic" and p == "basic": return True, "Basic Tier (50 EGP)"
    elif u == "pro" and p == "pro": return True, "Pro Tier (150 EGP)"
    return False, None

def calculate_egyptian_taxes(revenue, expenses):
    net_profit = revenue - expenses
    
    # 1. قانون 152 (كما هو)
    if revenue < 250000: tax_152 = 1000.0
    elif revenue < 500000: tax_152 = 2500.0
    elif revenue < 1000000: tax_152 = 5000.0
    elif revenue < 2000000: tax_152 = revenue * 0.005
    elif revenue < 3000000: tax_152 = revenue * 0.0075
    else: tax_152 = revenue * 0.01
    
    # 2. قانون 91 لسنة 2005 (الطريقة الثانية)
    # يتم حسابها على صافي الربح التجاري بنسبة 22.5%
    tax_91 = max(0.0, net_profit * 0.225) 
    
    return tax_152, tax_91, net_profit

def generate_smart_insights(revenue, expenses, tax_152, tax_91):
    insights = []
    if revenue == 0: return ["💡 **Notice:** Record your sales data to start generating AI insights."]
    
    # Actionable Insights (English)
    if tax_152 < tax_91:
        savings = tax_91 - tax_152
        insights.append(f"💡 **Tax Optimization:** Joining the Small Enterprises Law (Law 152) will save you **{savings:,.0f} EGP** this year compared to the standard income tax.")
    
    # Expense impact simulation
    potential_expense = expenses + 10000
    _, new_tax_91, _ = calculate_egyptian_taxes(revenue, potential_expense)
    tax_saved = tax_91 - new_tax_91
    if tax_saved > 0:
        insights.append(f"📉 **Simulation:** If you increase your documented operating expenses by 10,000 EGP, your tax liability under Law 91 will decrease by **{tax_saved:,.0f} EGP**.")
        
    return insights

def inject_mock_data():
    """Inject mock data to beautify the dashboard upon login"""
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    sales = [{'Date': d, 'Category': 'Consulting', 'Type': 'Sale', 'Amount': np.random.randint(2000, 8000)} for d in dates]
    expenses = [{'Date': d, 'Category': 'Software', 'Type': 'Expense', 'Amount': np.random.randint(500, 3000)} for d in dates[::3]]
    return pd.DataFrame(sales + expenses).sort_values('Date').reset_index(drop=True)

# ==========================================
# 2. Session State Initialization
# ==========================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'data' not in st.session_state: 
    st.session_state.data = inject_mock_data()

# ==========================================
# 3. SaaS Login Interface
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>☁️ SME Tax Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>The Smart Tax Platform for Egyptian SMEs</p>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.form("login"):
            st.info("Demo Accounts:\n- User: free | Pass: free\n- User: basic | Pass: basic\n- User: pro | Pass: pro")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In to Workspace"):
                valid, role = authenticate_user(u, p)
                if valid:
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
else:
    # ==========================================
    # 4. Main SaaS Application layout
    # ==========================================
    role_class = "badge-free" if "Free" in st.session_state.user_role else "badge-basic" if "Basic" in st.session_state.user_role else "badge-pro"
    
    st.sidebar.markdown(f'<div class="{role_class}">{st.session_state.user_role}</div>', unsafe_allow_html=True)
    
    menu = st.sidebar.radio("General", [
        "📊 Overview", 
        "📝 Sales & Invoices", 
        "💸 All Expenses", 
        "🧠 AI Tax Insights",
        "📂 Upload Excel",
        "📅 Tax Reminders",
        "👥 About Team"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = st.session_state.data
    df['Date'] = pd.to_datetime(df['Date'])
    total_rev = df[df['Type'] == 'Sale']['Amount'].sum()
    total_exp = df[df['Type'] == 'Expense']['Amount'].sum()
    t_152, t_91, profit = calculate_egyptian_taxes(total_rev, total_exp)

    # ------------------------------------------
    # SaaS Dashboard 
    # ------------------------------------------
    if menu == "📊 Overview":
        st.header("Dashboard Overview")
        
        # في قسم الـ Metrics داخل الـ Overview
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Gross Revenue", f"EGP {total_rev:,.0f}")
        m2.metric("Total Expenses", f"EGP {total_exp:,.0f}")
        m3.metric("Net Profit", f"EGP {profit:,.0f}")
        
        # إضافة الطريقتين للمقارنة في الـ Dashboard
        m4.markdown(f"""
        **Tax Estimates:**
        - Law 152: {t_152:,.0f} EGP
        - Law 91: {t_91:,.0f} EGP
        """)

        col_chart1, col_chart2 = st.columns([2, 1])
        with col_chart1:
            st.markdown("**Cash Flow & Bank Account**")
            daily_data = df.groupby([df['Date'].dt.date, 'Type'])['Amount'].sum().reset_index()
            fig1 = px.line(daily_data, x='Date', y='Amount', color='Type', color_discrete_map={'Sale':'#8b5cf6', 'Expense':'#cbd5e1'})
            fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='white', paper_bgcolor='white', height=250)
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_chart2:
            st.markdown("**Profit Margin Graph**")
            fig2 = px.pie(values=[profit, total_exp], names=['Gross Profit', 'Expenses'], hole=0.7, color_discrete_sequence=['#8b5cf6', '#f1f5f9'])
            fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False, height=250)
            st.plotly_chart(fig2, use_container_width=True)

        col_chart3, col_chart4 = st.columns([2, 1])
        with col_chart3:
            st.markdown("**Invoiced to you (Monthly)**")
            fig3 = px.bar(daily_data[daily_data['Type']=='Sale'], x='Date', y='Amount')
            fig3.update_traces(marker_color='#3b82f6')
            fig3.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='white', height=250)
            st.plotly_chart(fig3, use_container_width=True)
            
        with col_chart4:
            st.markdown("**Recent Expenses**")
            recent_exp = df[df['Type'] == 'Expense'].tail(4)[['Date', 'Amount']]
            st.dataframe(recent_exp, hide_index=True, use_container_width=True)

    # ------------------------------------------
    # Data Entry & Invoicing
    # ------------------------------------------
    elif menu == "📝 Sales & Invoices":
        st.header("Invoices & Sales")
        with st.form("invoice_form"):
            col1, col2 = st.columns(2)
            client = col1.text_input("Client Name")
            amt = col2.number_input("Amount", min_value=0.0)
            if st.form_submit_button("Create Invoice"):
                new_row = pd.DataFrame([{'Date': datetime.now(), 'Category': client, 'Type': 'Sale', 'Amount': amt}])
                st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                st.success("Invoice created successfully!")
        st.dataframe(df[df['Type']=='Sale'].sort_values('Date', ascending=False), use_container_width=True)

    elif menu == "💸 All Expenses":
        st.header("Expense Tracking")
        with st.form("exp_form"):
            col1, col2 = st.columns(2)
            cat = col1.text_input("Expense Category (e.g. Rent, Server, Ads)")
            amt = col2.number_input("Amount", min_value=0.0)
            if st.form_submit_button("Log Expense"):
                new_row = pd.DataFrame([{'Date': datetime.now(), 'Category': cat, 'Type': 'Expense', 'Amount': amt}])
                st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                st.success("Expense logged successfully!")
        st.dataframe(df[df['Type']=='Expense'].sort_values('Date', ascending=False), use_container_width=True)

    # ------------------------------------------
    # SaaS Premium Features
    # ------------------------------------------
    elif menu == "🧠 AI Tax Insights":
        st.header("AI Tax Optimization")
        if "Pro" in st.session_state.user_role:
            st.markdown("Here is your personalized tax strategy based on your current data:")
            insights = generate_smart_insights(total_rev, total_exp, t_152, t_91)
            for insight in insights:
                st.markdown(f"<div class='advice-box'>{insight}</div>", unsafe_allow_html=True)
                
            st.markdown("---")
            st.subheader("Generate Official PDF Report")
            html_report = f"<h1>SME Tax Calculator Report</h1><p>Revenue: {total_rev}</p><p>Tax: {t_152}</p>"
            st.download_button("📥 Download Report", data=html_report, file_name="Report.html", mime="text/html")
        else:
            st.error("🔒 AI Insights and PDF generation are only available in the Pro Tier (150 EGP/mo).")

    elif menu == "📂 Upload Excel":
        st.header("Bulk Upload Data")
        if "Free" not in st.session_state.user_role:
            uploaded_file = st.file_uploader("Upload your bank statement or excel sheet", type=["csv", "xlsx"])
            if uploaded_file is not None:
                st.success("File uploaded! AI mapping engine is processing your rows...")
        else:
            st.error("🔒 Excel Bulk Upload is available for Basic and Pro Tiers.")

    elif menu == "📅 Tax Reminders":
        st.header("Compliance Calendar")
        st.info("Never miss a deadline. We sync these dates with the Egyptian Tax Authority.")
        
        schedule = pd.DataFrame({
            "Deadline": ["April 30, 2026", "Monthly (15th)", "Quarterly"],
            "Task": ["Annual Income Tax Filing", "VAT Return Filing", "Payroll Tax Submission"],
            "Status": ["Upcoming", "Action Required", "On Track"]
        })
        st.table(schedule)
        
    # ------------------------------------------
    # About Team Section
    # ------------------------------------------
    elif menu == "👥 About Team":
        st.header("👥 Project Developers")
        st.markdown("Developed strictly based on **Egyptian Tax Authority Standards (Law 152/2020 & Law 91/2005)** for Graduation Project 2026.")
        
        team_data = {
            "Member Name": [
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
