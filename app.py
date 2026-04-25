import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. الإعدادات الأساسية
API_KEY = "AIzaSyD7FvVcME2hyYWrLT31u3Ufdeoc3LjjYfQ"

def get_chat_response(prompt):
    """دالة تحاول استدعاء الموديلات المتاحة بالترتيب لضمان العمل"""
    genai.configure(api_key=API_KEY)
    
    # قائمة الموديلات للتبديل بينها في حال فشل أحدها
    models_to_try = ['gemini-1.5-flash-exp', 'gemini-pro', 'gemini-1.5-flash']
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            continue # إذا فشل موديل ينتقل للذي يليه
    return "عذراً، خدمة الذكاء الاصطناعي غير متاحة حالياً في منطقتك. يرجى المحاولة لاحقاً."

# 2. إعدادات الصفحة
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- القائمة الجانبية ---
st.sidebar.title("SME Tax Expert")
page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", 
    "2. Operating Expenses", 
    "3. Tax Dashboard & Report",
    "4. Smart Tax Assistant 🤖",
    "5. About the Project"
])

# ==========================
# الوظائف المالية (نفس كودك الأصلي)
# ==========================
if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management")
    with st.form("add_sale"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Client")
        amt = c2.number_input("Amount (EGP)", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.sales_data.append({"Client": name, "Amount": amt})
    st.dataframe(pd.DataFrame(st.session_state.sales_data))

elif page == "2. Operating Expenses":
    st.title("💸 Expenses")
    with st.form("add_exp"):
        item = st.text_input("Item")
        cost = st.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("Record"):
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
    st.dataframe(pd.DataFrame(st.session_state.expenses_data))

elif page == "3. Tax Dashboard & Report":
    st.title("📊 Tax Dashboard")
    rev = sum(d['Amount'] for d in st.session_state.sales_data)
    exp = sum(d['Cost'] for d in st.session_state.expenses_data)
    st.metric("Net Profit", f"{rev - exp:,.2f} EGP")
    st.success(f"Law 152 Tax: {5000 if rev < 1000000 else rev * 0.01:,.2f} EGP")

# ==========================
# الذكاء الاصطناعي (الحل الأكيد)
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = get_chat_response(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

elif page == "5. About the Project":
    st.title("Team Credits")
    team = pd.DataFrame({
        "Name": ["Omar Mohamed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    })
    st.table(team)
