import streamlit as st
import pandas as pd
import requests
import json

# 1. الإعدادات والذكاء الاصطناعي
# استخدمنا المفتاح الذي نجح في التيست الخاص بك
API_KEY = "AIzaSyD7FvVcME2hyYWrLT31u3Ufdeoc3LjjYfQ"

def get_ai_response(prompt):
    # استخدام الرابط المباشر لتجنب مشاكل المكتبات
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-exp:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"You are an Egyptian tax expert. Answer professionally: {prompt}"}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "الخدمة مشغولة حالياً، يرجى المحاولة بعد لحظات."
    except:
        return "عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي."

# 2. إعدادات الصفحة
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# تهيئة البيانات
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- Sidebar ---
st.sidebar.title("SME Tax Expert")
st.sidebar.markdown("Graduation Project 2026")

page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", 
    "2. Operating Expenses", 
    "3. Tax Dashboard & Report",
    "4. Smart Tax Assistant 🤖",
    "5. About the Project"
])

# ==========================
# 1. Sales Module
# ==========================
if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management")
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("Saved!")
    st.dataframe(pd.DataFrame(st.session_state.sales_data), use_container_width=True)

# ==========================
# 2. Expenses Module
# ==========================
elif page == "2. Operating Expenses":
    st.title("💸 Expenses")
    with st.form("add_exp"):
        item = st.text_input("Item")
        cost = st.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("Record"):
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("Recorded!")
    st.dataframe(pd.DataFrame(st.session_state.expenses_data), use_container_width=True)

# ==========================
# 3. Dashboard
# ==========================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Tax Dashboard")
    rev = sum(d['Amount'] for d in st.session_state.sales_data)
    exp = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = rev - exp
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Revenue", f"{rev:,.2f}")
    c2.metric("Expenses", f"{exp:,.2f}")
    c3.metric("Profit", f"{profit:,.2f}")

    st.markdown("---")
    tax_152 = 5000 if rev < 1000000 else rev * 0.01
    st.info(f"Estimated Tax (Law 152): EGP {tax_152:,.2f}")

# ==========================
# 4. AI Assistant
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# ==========================
# 5. Team
# ==========================
elif page == "5. About the Project":
    st.title("Project Team")
    team = pd.DataFrame({
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"]
    })
    st.table(team)
