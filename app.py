import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="SME Mini ERP", layout="wide")

# --- تجهيز الذاكرة (Database Simulation) ---
# دي خطوة مهمة عشان البرنامج "يفتكر" البيانات لما تتنقل بين الصفحات
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state:
    st.session_state.expenses_data = []

# --- القائمة الجانبية (ERP Menu) ---
st.sidebar.title("🏢 SME ERP System")
page = st.sidebar.radio("القائمة الرئيسية", ["1. تسجيل المبيعات (Sales)", "2. تسجيل المصروفات (Expenses)", "3. المركز المالي والضرائب (Tax & Dashboard)"])

# ==========================
# 1. صفحة المبيعات (Sales)
# ==========================
if page == "1. تسجيل المبيعات (Sales)":
    st.header("🛒 إدارة المبيعات والفواتير")
    
    # نموذج إدخال فاتورة
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client_name = col1.text_input("اسم العميل")
        amount = col2.number_input("قيمة الفاتورة (EGP)", min_value=0.0, step=100.0)
        submit_sale = st.form_submit_button("حفظ الفاتورة")
        
        if submit_sale and amount > 0:
            st.session_state.sales_data.append({"العميل": client_name, "المبلغ": amount})
            st.success("تم تسجيل الفاتورة بنجاح! ✅")

    # عرض جدول المبيعات
    if st.session_state.sales_data:
        st.subheader("سجل الفواتير")
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df_sales, use_container_width=True)
        st.metric("إجمالي المبيعات", f"{df_sales['المبلغ'].sum():,.2f} EGP")
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")

# ==========================
# 2. صفحة المصروفات (Expenses)
# ==========================
elif page == "2. تسجيل المصروفات (Expenses)":
    st.header("💸 إدارة المصروفات")
    
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        desc = col1.text_input("بند المصروف (إيجار، كهرباء...)")
        cost = col2.number_input("التكلفة (EGP)", min_value=0.0, step=100.0)
        submit_exp = st.form_submit_button("تسجيل المصروف")
        
        if submit_exp and cost > 0:
            st.session_state.expenses_data.append({"البند": desc, "التكلفة": cost})
            st.success("تم تسجيل المصروف بنجاح! ✅")

    if st.session_state.expenses_data:
        st.subheader("سجل المصروفات")
        df_exp = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_exp, use_container_width=True)
        st.metric("إجمالي المصروفات", f"{df_exp['التكلفة'].sum():,.2f} EGP")
    else:
        st.info("لا توجد مصروفات مسجلة.")

# ==========================
# 3. صفحة الضرائب (Dashboard)
# ==========================
elif page == "3. المركز المالي والضرائب (Tax & Dashboard)":
    st.header("📊 الموقف المالي والضريبي")

    # تجميع الأرقام أوتوماتيكياً (Integration)
    total_sales = sum(item['المبلغ'] for item in st.session_state.sales_data)
    total_expenses = sum(item['التكلفة'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses

    # عرض الملخص
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الإيرادات", f"{total_sales:,.2f} EGP")
    col2.metric("إجمالي المصروفات", f"{total_expenses:,.2f} EGP")
    col3.metric("صافي الربح المحاسبي", f"{net_profit:,.2f} EGP", delta_color="normal")

    st.markdown("---")
    st.subheader("⚖️ الحساب الضريبي (SME Tax Calculation)")

    # 1. النظام المبسط (قانون 152)
    st.markdown("#### 1️⃣ أولاً: وفقاً للنظام المبسط (قانون 152 لسنة 2020)")
    tax_152 = 0
    desc_152 = ""
    
    if total_sales == 0:
        st.warning("يرجى تسجيل مبيعات أولاً لحساب الضريبة.")
    else:
        if total_sales < 250000: tax_152, desc_152 = 1000, "فئة ثابتة"
        elif total_sales < 500000: tax_152, desc_152 = 2500, "فئة ثابتة"
        elif total_sales < 1000000: tax_152, desc_152 = 5000, "فئة ثابتة"
        elif total_sales < 2000000: tax_152, desc_152 = total_sales * 0.005, "نسبة 0.5%"
        elif total_sales < 3000000: tax_152, desc_152 = total_sales * 0.0075, "نسبة 0.75%"
        elif total_sales <= 10000000: tax_152, desc_152 = total_sales * 0.01, "نسبة 1%"
        
        if tax_152 > 0:
            st.success(f"الضريبة المستحقة (مبسط): {tax_152:,.2f} جنيه ({desc_152})")
        else:
            st.error("خارج نطاق المشروعات الصغيرة (> 10 مليون)")

    # 2. النظام العام (قانون 91)
    st.markdown("#### 2️⃣ ثانياً: وفقاً للنظام العام (قانون 91 لسنة 2005)")
    tax_91 = max(0, net_profit * 0.225)
    st.info(f"الضريبة المستحقة (عام): {tax_91:,.2f} جنيه (22.5% من صافي الربح)")

    # التوصية
    if total_sales > 0:
        st.markdown("### 💡 التوصية الذكية")
        if tax_152 > 0 and tax_152 < tax_91:
            st.write(f"ننصحك بالنظام المبسط لأنه سيوفر عليك **{tax_91 - tax_152:,.2f} جنيه**.")
        elif tax_91 < tax_152:
            st.write("النظام العام قد يكون أفضل لك (خاصة إذا كانت المصروفات مرتفعة).")