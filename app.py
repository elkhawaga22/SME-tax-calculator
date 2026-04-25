import streamlit as st
import pandas as pd

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("🇪🇬 SME Tax Expert")
st.sidebar.markdown("**Graduation Project 2026**")

page = st.sidebar.radio("القوائم", ["🛒 المبيعات", "💸 المصروفات", "📊 لوحة الضرائب", "👥 الفريق"])

# 1. Sales
if page == "🛒 المبيعات":
    st.title("🛒 إدارة المبيعات والفواتير")
    
    with st.form("sales_form"):
        col1, col2, col3 = st.columns(3)
        client = col1.text_input("اسم العميل")
        date = col2.date_input("التاريخ")
        amount = col3.number_input("قيمة الفاتورة (جنيه)", min_value=0.0)
        
        col_btn, col_clear = st.columns(2)
        with col_btn:
            save = st.form_submit_button("💾 حفظ الفاتورة", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("🗑️ مسح", use_container_width=True)
        
        if save and amount > 0:
            st.session_state.sales_data.append({
                "Client": client, 
                "Date": date, 
                "Amount": amount
            })
            st.success("✅ تم حفظ الفاتورة!")
            st.rerun()
        if clear:
            st.session_state.sales_data = []
            st.success("🗑️ تم مسح البيانات")
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي المبيعات", f"{df['Amount'].sum():,.0f} جنيه")
        col2.metric("عدد الفواتير", f"{len(df)}")
        col3.metric("متوسط الفاتورة", f"{df['Amount'].mean():,.0f} جنيه")

# 2. Expenses
elif page == "💸 المصروفات":
    st.title("💸 إدارة المصروفات التشغيلية")
    
    with st.form("expenses_form"):
        col1, col2, col3 = st.columns(3)
        category = col1.selectbox("الفئة", ["إيجار", "كهرباء", "رواتب", "صيانة", "أخرى"])
        item = col2.text_input("تفاصيل المصروف")
        cost = col3.number_input("التكلفة (جنيه)", min_value=0.0)
        
        col_btn, col_clear = st.columns(2)
        with col_btn:
            save = st.form_submit_button("💾 تسجيل المصروف", use_container_width=True)
        with col_clear:
            clear = st.form_submit_button("🗑️ مسح", use_container_width=True)
        
        if save and cost > 0:
            st.session_state.expenses_data.append({
                "Category": category,
                "Item": item,
                "Cost": cost
            })
            st.success("✅ تم تسجيل المصروف!")
            st.rerun()
        if clear:
            st.session_state.expenses_data = []
            st.success("🗑️ تم مسح البيانات")
            st.rerun()
    
    if st.session_state.expenses_data:
        df = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("إجمالي المصروفات", f"{df['Cost'].sum():,.0f} جنيه")

# 3. Dashboard
elif page == "📊 لوحة الضرائب":
    st.title("📊 لوحة تحكم الضرائب")
    
    sales_total = sum(d['Amount'] for d in st.session_state.sales_data)
    expenses_total = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = sales_total - expenses_total
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 إجمالي المبيعات", f"{sales_total:,.0f} جنيه")
    col2.metric("💸 إجمالي المصروفات", f"{expenses_total:,.0f} جنيه")
    col3.metric("💵 صافي الربح", f"{profit:,.0f} جنيه")
    col4.metric("📈 هامش الربح", f"{(profit/sales_total*100):.1f}%" if sales_total > 0 else "0%")
    
    # Tax Calculations
    st.subheader("💼 حسابات الضرائب")
    tab1, tab2 = st.tabs(["قانون 152/2021 (مبسط)", "قانون 91/2005 (عام)"])
    
    with tab1:
        st.info("**نظام الضريبة المبسط للشركات الصغيرة**")
        if sales_total < 1000000:
            tax_152 = 5000
            st.success(f"✅ الضريبة الثابتة: **5,000 جنيه**")
        elif sales_total < 5000000:
            tax_152 = sales_total * 0.01
            st.success(f"✅ نسبة 1%: **{tax_152:,.0f} جنيه**")
        else:
            tax_152 = sales_total * 0.015
            st.success(f"✅ نسبة 1.5%: **{tax_152:,.0f} جنيه**")
    
    with tab2:
        st.warning("**النظام العام للضرائب**")
        taxable_profit = max(0, profit * 0.8)  # بعد الخصومات
        tax_91 = taxable_profit * 0.225
        st.warning(f"💰 الضريبة المتوقعة (22.5%): **{tax_91:,.0f} جنيه**")

# 4. Team
elif page == "👥 الفريق":
    st.title("👥 فريق المشروع")
    st.markdown("""
    # SME Tax Expert
    **مشروع تخرج 2026**
    
    
