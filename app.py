import streamlit as st
import pandas as pd

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state:
    st.session_state.expenses_data = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("🇪🇬 SME Tax Expert")
st.sidebar.markdown("Graduation Project 2026")

page = st.sidebar.radio("القوائم", [
    "1️⃣ المبيعات والفواتير", 
    "2️⃣ المصروفات التشغيلية", 
    "3️⃣ لوحة الضرائب المتكاملة",
    "4️⃣ الفريق والمعلومات"
])

# ========================================
# 1. SALES & INVOICING MODULE
# ========================================
if page == "1️⃣ المبيعات والفواتير":
    st.title("🛒 إدارة المبيعات والفواتير")
    
    with st.form("sales_form"):
        col1, col2, col3 = st.columns(3)
        client_name = col1.text_input("📝 اسم العميل")
        invoice_date = col2.date_input("📅 تاريخ الفاتورة")
        invoice_amount = col3.number_input("💰 قيمة الفاتورة (جنيه)", min_value=0.0)
        
        col_save, col_clear = st.columns(2)
        with col_save:
            save_invoice = st.form_submit_button("💾 حفظ الفاتورة", use_container_width=True)
        with col_clear:
            clear_sales = st.form_submit_button("🗑️ مسح جميع الفواتير", use_container_width=True)
        
        if save_invoice and invoice_amount > 0:
            st.session_state.sales_data.append({
                "Client": client_name,
                "Date": invoice_date,
                "Amount": invoice_amount
            })
            st.success("✅ تم حفظ الفاتورة بنجاح!")
            st.balloons()
            st.rerun()
        
        if clear_sales:
            st.session_state.sales_data = []
            st.success("🗑️ تم مسح جميع الفواتير")
            st.rerun()
    
    # Display sales data
    if st.session_state.sales_data:
        st.subheader("📋 سجل الفواتير")
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df_sales, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 إجمالي المبيعات", f"{df_sales['Amount'].sum():,.0f} جنيه")
        col2.metric("📊 عدد الفواتير", len(df_sales))
        col3.metric("📈 متوسط الفاتورة", f"{df_sales['Amount'].mean():,.0f} جنيه")

# ========================================
# 2. OPERATING EXPENSES MODULE
# ========================================
elif page == "2️⃣ المصروفات التشغيلية":
    st.title("💸 إدارة المصروفات التشغيلية")
    
    with st.form("expenses_form"):
        col1, col2, col3 = st.columns(3)
        expense_category = col1.selectbox(
            "🏷️ فئة المصروف", 
            ["إيجار", "كهرباء/مياه", "رواتب موظفين", "صيانة معدات", "تسويق", "نقل", "أخرى"]
        )
        expense_item = col2.text_input("📝 وصف المصروف")
        expense_cost = col3.number_input("💰 التكلفة (جنيه)", min_value=0.0)
        
        col_save, col_clear = st.columns(2)
        with col_save:
            save_expense = st.form_submit_button("💾 تسجيل المصروف", use_container_width=True)
        with col_clear:
            clear_expenses = st.form_submit_button("🗑️ مسح جميع المصروفات", use_container_width=True)
        
        if save_expense and expense_cost > 0:
            st.session_state.expenses_data.append({
                "Category": expense_category,
                "Item": expense_item,
                "Cost": expense_cost
            })
            st.success("✅ تم تسجيل المصروف بنجاح!")
            st.rerun()
        
        if clear_expenses:
            st.session_state.expenses_data = []
            st.success("🗑️ تم مسح جميع المصروفات")
            st.rerun()
    
    # Display expenses data
    if st.session_state.expenses_data:
        st.subheader("📋 سجل المصروفات")
        df_expenses = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_expenses, use_container_width=True, hide_index=True)
        st.metric("💸 إجمالي المصروفات", f"{df_expenses['Cost'].sum():,.0f} جنيه")

# ========================================
# 3. TAX DASHBOARD & REPORTS
# ========================================
elif page == "3️⃣ لوحة الضرائب المتكاملة":
    st.title("📊 لوحة تحكم الضرائب المتكاملة")
    
    # Calculate totals
    sales_total = sum(d['Amount'] for d in st.session_state.sales_data)
    expenses_total = sum(d['Cost'] for d in st.session_state.expenses_data)
    net_profit = sales_total - expenses_total
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 إجمالي المبيعات", f"{sales_total:,.0f} جنيه")
    col2.metric("💸 إجمالي المصروفات", f"{expenses_total:,.0f} جنيه")
    col3.metric("💵 صافي الربح", f"{net_profit:,.0f} جنيه")
    col4.metric("📈 هامش الربح", f"{(net_profit/sales_total*100):.1f}%" if sales_total > 0 else "0%")
    
    # Tax calculations
    st.subheader("💼 حسابات الضرائب المصرية")
    
    col_law152, col_law91 = st.columns(2)
    
    with col_law152:
        st.info("**🏢 قانون 152/2021 - النظام المبسط**")
        if sales_total < 1000000:
            tax_152 = 5000
            rate = "ثابت 5,000 جنيه"
        elif sales_total < 5000000:
            tax_152 = sales_total * 0.01
            rate = "1% من المبيعات"
        else:
            tax_152 = sales_total * 0.015
            rate = "1.5% من المبيعات"
        st.success(f"**الضريبة: {tax_152:,.0f} جنيه**\n({rate})")
    
    with col_law91:
        st.warning("**📜 قانون 91/2005 - النظام العام**")
        taxable_profit = max(0, net_profit * 0.8)  # بعد الخصومات
        tax_91 = taxable_profit * 0.225
        st.warning(f"**الضريبة: {tax_91:,.0f} جنيه**\n(22.5% من الربح الخاضع للضريبة)")

# ========================================
# 4. TEAM & PROJECT INFO
# ========================================
elif page == "4️⃣ الفريق والمعلومات":
    st.title("👥 فريق المشروع")
    
    st.markdown("""
    # **SME Tax Expert**
    **مشروع تخرج 2026**
    
    ## 🧑‍💼 الأعضاء:
    
    
