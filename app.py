import streamlit as st
import pandas as pd
import google.generativeai as genai

# ==========================
# 1. Configuration & AI Setup
# ==========================
# المفتاح الجديد الذي استخرجته
API_KEY = "AIzaSyACmy1UgjAVZBpf1sxPAvm0vap8cF_n08Q"

def initialize_ai():
    try:
        genai.configure(api_key=API_KEY)
        # استخدام النسخة المستقرة والأحدث
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
        return None

model = initialize_ai()

# ==========================
# 2. Page Configuration
# ==========================
st.set_page_config(page_title="SME Tax Expert 2026", layout="wide", page_icon="🇪🇬")

# تهيئة مخزن البيانات في المتصفح
if 'sales' not in st.session_state: st.session_state.sales = []
if 'expenses' not in st.session_state: st.session_state.expenses = []
if 'messages' not in st.session_state: st.session_state.messages = []

# --- القائمة الجانبية ---
st.sidebar.title("🏢 SME Tax Expert")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", [
    "📊 Dashboard", 
    "🛒 Sales & Invoicing", 
    "💸 Expenses", 
    "🤖 Smart AI Assistant",
    "👥 Team Credits"
])

# ==========================
# 3. Modules Logic
# ==========================

# --- صفحة المبيعات ---
if menu == "🛒 Sales & Invoicing":
    st.header("Sales Management")
    with st.form("sale_form"):
        c1, c2 = st.columns(2)
        client = c1.text_input("Client Name")
        amount = c2.number_input("Amount (EGP)", min_value=0.0)
        if st.form_submit_button("Add Invoice") and amount > 0:
            st.session_state.sales.append({"Client": client, "Amount": amount})
            st.success("Invoice Saved! ✅")
    if st.session_state.sales:
        st.dataframe(pd.DataFrame(st.session_state.sales), use_container_width=True)

# --- صفحة المصروفات ---
elif menu == "💸 Expenses":
    st.header("Expense Tracking")
    with st.form("exp_form"):
        c1, c2 = st.columns(2)
        item = c1.text_input("Expense Item")
        cost = c2.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("Record Expense") and cost > 0:
            st.session_state.expenses.append({"Item": item, "Cost": cost})
            st.success("Expense Recorded! ✅")
    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

# --- لوحة التحكم ---
elif menu == "📊 Dashboard":
    st.header("Financial Overview")
    rev = sum(s['Amount'] for s in st.session_state.sales)
    exp = sum(e['Cost'] for e in st.session_state.expenses)
    profit = rev - exp
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"{rev:,.2f} EGP")
    col2.metric("Total Expenses", f"{exp:,.2f} EGP")
    col3.metric("Net Profit", f"{profit:,.2f} EGP")
    
    st.markdown("---")
    st.subheader("Estimated Egyptian Tax (Law 152)")
    # حساب تقريبي حسب القانون 152 للمشروعات الصغيرة
    tax = 5000 if rev < 1000000 else rev * 0.01
    st.info(f"Your estimated tax based on revenue is: **{tax:,.2f} EGP**")

# --- مساعد الذكاء الاصطناعي ---
elif menu == "🤖 Smart AI Assistant":
    st.header("Smart Tax Assistant 🤖")
    st.caption("Ask anything about Egyptian Tax Laws")
    
    # عرض تاريخ المحادثة
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            if model:
                try:
                    # توجيه الموديل للعمل كخبير ضرائب مصري
                    full_prompt = f"You are a professional Egyptian tax expert for SMEs. Respond to: {prompt}"
                    response = model.generate_content(full_prompt)
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"AI Error: {e}")
            else:
                st.error("AI Model not initialized correctly.")

# --- صفحة الفريق ---
elif menu == "👥 Team Credits":
    st.header("Project Team")
    team = pd.DataFrame({
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    })
    st.table(team)
