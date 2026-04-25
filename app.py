import streamlit as st
import pandas as pd
import io

# 1. إعدادات الصفحة العامة
st.set_page_config(
    page_title="SME Tax Expert 2026",
    layout="wide",
    page_icon="🇪🇬"
)

# تخصيص واجهة المستخدم بـ CSS بسيط لتحسين المظهر
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_name=True)

# --- تهيئة البيانات (Session State) ---
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []

# ==========================================
# محرك الحسابات الضريبية (Tax Engine)
# ==========================================

def calculate_taxes(revenue, expenses):
    profit = revenue - expenses
    
    # حساب قانون 152 (حسب حجم الأعمال)
    if revenue < 250000:
        tax_152 = 1000
        note_152 = "ضريبة قطعية: 1,000 ج.م سنويًا"
    elif revenue < 500000:
        tax_152 = 2500
        note_152 = "ضريبة قطعية: 2,500 ج.م سنويًا"
    elif revenue < 1000000:
        tax_152 = 5000
        note_152 = "ضريبة قطعية: 5,000 ج.م سنويًا"
    elif revenue < 2000000:
        tax_152 = revenue * 0.005
        note_152 = "نسبة 0.5% من حجم الأعمال"
    elif revenue < 3000000:
        tax_152 = revenue * 0.0075
        note_152 = "نسبة 0.75% من حجم الأعمال"
    else:
        tax_152 = revenue * 0.01
        note_152 = "نسبة 1.0% من حجم الأعمال"

    # حساب قانون 91 (22.5% من صافي الربح)
    tax_91 = max(0, profit * 0.225)
    note_91 = "نسبة 22.5% من صافي الأرباح التجارية"
    
    return tax_152, note_152, tax_91, note_91

# ==========================================
# القائمة الجانبية (Sidebar)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=100)
st.sidebar.title("SME Tax Expert")
st.sidebar.markdown("---")

menu = st.sidebar.radio("القائمة الرئيسية", [
    "🛒 تسجيل المبيعات",
    "💸 تسجيل المصروفات",
    "📊 لوحة التقارير والضرائب",
    "👥 فريق العمل والأهداف"
])

# ==========================================
# 1. صفحة المبيعات
# ==========================================
if menu == "🛒 تسجيل المبيعات":
    st.title("🛒 إدارة الفواتير والمبيعات")
    st.info("قم بتسجيل كافة مبيعات المنشأة خلال الفترة الضريبية.")
    
    with st.container():
        with st.form("sales_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            client = col1.text_input("اسم العميل / رقم الفاتورة")
            amount = col2.number_input("قيمة الفاتورة (ج.م)", min_value=0.0, format="%.2f")
            
            if st.form_submit_button("إضافة الفاتورة ✅"):
                if amount > 0:
                    st.session_state.sales_data.append({"البيان": client, "المبلغ": amount})
                    st.success("تم تسجيل الفاتورة بنجاح")
                else:
                    st.error("يرجى إدخال مبلغ صحيح")

    if st.session_state.sales_data:
        st.markdown("### سجل المبيعات الحالي")
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.table(df_sales)
        st.metric("إجمالي الإيرادات", f"{df_sales['المبلغ'].sum():,.2f} ج.م")

# ==========================================
# 2. صفحة المصروفات
# ==========================================
elif menu == "💸 تسجيل المصروفات":
    st.title("💸 إدارة المصروفات التشغيلية")
    st.info("سجل كافة التكاليف والمصروفات الإدارية والعمومية المرتبطة بالنشاط.")
    
    with st.form("expenses_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        item = col1.text_input("بند المصروف (إيجار، أجور، كهرباء...)")
        cost = col2.number_input("التكلفة (ج.م)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("تسجيل المصروف 💾"):
            if cost > 0:
                st.session_state.expenses_data.append({"البند": item, "التكلفة": cost})
                st.success("تم تسجيل المصروف بنجاح")

    if st.session_state.expenses_data:
        st.markdown("### سجل المصروفات الحالي")
        df_expenses = pd.DataFrame(st.session_state.expenses_data)
        st.table(df_expenses)
        st.metric("إجمالي المصروفات", f"{df_expenses['التكلفة'].sum():,.2f} ج.م")

# ==========================================
# 3. صفحة التقارير والضرائب
# ==========================================
elif menu == "📊 لوحة التقارير والضرائب":
    st.title("📊 التقرير المالي والضريبي الختامي")
    
    total_rev = sum(d['المبلغ'] for d in st.session_state.sales_data)
    total_exp = sum(d['التكلفة'] for d in st.session_state.expenses_data)
    net_profit = total_rev - total_exp
    
    # عرض المؤشرات المالية الأساسية
    st.markdown("### ملخص الأداء المالي")
    m1, m2, m3 = st.columns(3)
    m1.metric("إجمالي الإيرادات", f"{total_rev:,.2f} ج.م")
    m2.metric("إجمالي المصروفات", f"{total_exp:,.2f} ج.م")
    m3.metric("صافي الربح/الخسارة", f"{net_profit:,.2f} ج.م", delta=f"{net_profit:,.2f}")

    st.markdown("---")
    
    # حساب الضرائب وعرضها
    tax_152, note_152, tax_91, note_91 = calculate_taxes(total_rev, total_exp)
    
    st.markdown("### المقارنة الضريبية (طبقاً للتشريعات المصرية)")
    t1, t2 = st.columns(2)
    
    with t1:
        st.subheader("🏢 قانون 152 (المبسط)")
        st.success(f"الضريبة المستحقة: {tax_152:,.2f} ج.م")
        st.caption(f"الأساس: {note_152}")
        
    with t2:
        st.subheader("📝 قانون 91 (الدخل)")
        st.warning(f"الضريبة المستحقة: {tax_91:,.2f} ج.م")
        st.caption(f"الأساس: {note_91}")

    # ميزة تحميل التقرير
    full_report = f"""
    === تقرير SME Tax Expert المالي 2026 ===
    إجمالي الإيرادات: {total_rev:,.2f} ج.م
    إجمالي المصروفات: {total_exp:,.2f} ج.م
    صافي الربح: {net_profit:,.2f} ج.م
    ---------------------------------------
    تحليل الضرائب المستحقة:
    1. قانون 152 لعام 2020: {tax_152:,.2f} ج.م ({note_152})
    2. قانون 91 لعام 2005: {tax_91:,.2f} ج.م ({note_91})
    ---------------------------------------
    * تم استخراج هذا التقرير طبقاً لمعايير مصلحة الضرائب المصرية *
    """
    
    st.markdown("---")
    st.download_button(
        label="📥 تحميل التقرير المالي كملف نصي",
        data=full_report,
        file_name="Tax_Full_Report.txt",
        mime="text/plain"
    )

# ==========================================
# 4. صفحة فريق العمل والأهداف (المكان المطلوب)
# ==========================================
elif menu == "👥 فريق العمل والأهداف":
    st.title("👥 فريق عمل المشروع")
    
    # عرض فريق العمل في جدول منظم
    team_data = {
        "الاسم الكامل": [
            "Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", 
            "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", 
            "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"
        ],
        "كود الطالب": [
            "2202297", "2200216", "2200243", 
            "2200236", "2200190", "2202312", 
            "2200137", "2200176", "2202995"
        ]
    }
    st.table(pd.DataFrame(team_data))
    
    st.markdown("---")
    
    # أهداف المشروع (كما طلبت في نهاية الصفحة)
    st.header("🎯 أهداف المشروع")
    st.markdown("""
    1. **التحول الرقمي:** المساهمة في رؤية مصر 2030 من خلال رقمنة العمليات المحاسبية للمشروعات الصغيرة.
    2. **دعم اتخاذ القرار:** تمكين صاحب المشروع من المقارنة بين الأنظمة الضريبية المختلفة لاختيار الأنسب له.
    3. **الدقة المحاسبية:** تقليل الأخطاء البشرية في حساب الشرائح الضريبية المعقدة.
    4. **التوعية الضريبية:** تبسيط القوانين المصرية (152 و 91) للمستخدم العادي.
    """)
    
    # الإخلاء القانوني والتبعية لمصلحة الضرائب
    st.markdown("---")
    st.subheader("⚖️ مرجعية النظام")
    st.info("""
    جميع المعادلات والموازين الضريبية المستخدمة في هذا النظام تم برمجتها وفقاً لآخر التحديثات الصادرة عن **مصلحة الضرائب المصرية**.
    * **قانون رقم 152 لسنة 2020:** المنظم للمشروعات الصغيرة والمتوسطة.
    * **قانون رقم 91 لسنة 2005:** وتعديلاته الخاصة بالضريبة على الدخل.
    """)
    st.caption("تم تطوير هذا العمل كمتطلب لمشروع التخرج لعام 2026.")
