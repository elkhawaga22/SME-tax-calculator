import streamlit as st
import pandas as pd

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state:
    st.session_state.expenses_data = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("SME Tax Expert")
st.sidebar.markdown("Graduation Project 2026")

page = st.sidebar.radio("القوائم", ["المبيعات", "المصروفات", "لوحة الضرائب", "الفريق"])

# 1. Sales
if page == "المبيعات":
    st.title("🛒 المبيعات والفواتير")
    
    with st.form("sales"):
        col1, col2 = st.columns(2)
        client = col1.text_input("اسم العميل")
        amount = col2.number_input("قيمة الفاتورة", min_value=0.0)
        submitted = st.form_submit_button("حفظ")
        
        if submitted and amount > 0:
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("تم الحفظ!")
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df)
        st.metric("الإجمالي", f"{df['Amount'].sum():,.0f} جنيه")
    
    if st.button("مسح الكل"):
        st.session_state.sales_data = []
        st.rerun()

# 2. Expenses
elif page == "المصروفات":
    st.title("💸 المصروفات")
    
    with st.form("expenses"):
        col1, col2 = st.columns(2)
        item = col1.text_input("المصروف")
        cost = col2.number_input("التكلفة", min_value=0.0)
        submitted = st.form_submit_button("حفظ")
        
        if submitted and cost > 0:
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("تم الحفظ!")
            st.rerun()
    
    if st.session_state.expenses_data:
        df = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df)
        st.metric("الإجمالي", f"{df['Cost'].sum():,.0f} جنيه")
    
    if st.button("مسح الكل"):
        st.session_state.expenses_data = []
        st.rerun()

# 3. Dashboard
elif page == "لوحة الضرائب":
    st.title("📊 لوحة الضرائب")
    
    sales = sum(d['Amount'] for d in st.session_state.sales_data)
    expenses = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = sales - expenses
    
    col1, col2, col3 = st.columns(3)
    col1.metric("المبيعات", f"{sales:,.0f} ج")
    col2.metric("المصروفات", f"{expenses:,.0f} ج")
    col3.metric("الربح", f"{profit:,.0f} ج")
    
    st.subheader("حسابات الضرائب")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("قانون 152")
        tax152 = 5000 if sales < 1000000 else sales * 0.01
        st.success(f"{tax152:,.0f} جنيه")
    
    with col2:
        st.warning("قانون 91")
        tax91 = max(0, profit * 0.225)
        st.warning(f"{tax91:,.0f} جنيه")

# 4. Team
elif page == "الفريق":
    st.title("👥 الفريق")
    
    st.markdown("""
    **SME Tax Expert**
    
    - عمر محمد أحمد (2202297)
    - منة الله معمن (2200216)
    - مريز أدهم (2200243)
    """)

    st.balloons()
