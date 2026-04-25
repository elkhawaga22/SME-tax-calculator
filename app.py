import streamlit as st
import pandas as pd
import requests
import json

# 1. Configuration
# تأكد من استخدام هذا المفتاح الجديد أو الذي عمل معك في التيست
API_KEY = "AIzaSyD7FvVcME2hyYWrLT31u3Ufdeoc3LjjYfQ"

def get_ai_response(prompt):
    # استخدام رابط مباشر (v1beta) مع الموديل التجريبي الذي نجح في التيست عندك
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-exp:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"You are an Egyptian tax expert. Answer professionally: {prompt}"}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        if "candidates" in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # محاولة بديلة بموديل gemini-pro إذا فشل الأول
            url_pro = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
            response = requests.post(url_pro, headers=headers, data=json.dumps(payload))
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {str(e)}"

# 2. Page Setup
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# Sidebar
st.sidebar.title("SME Tax Expert")
page = st.sidebar.radio("Navigation", ["1. Financial Modules", "2. Smart Tax Assistant 🤖", "3. Team"])

# --- Modules ---
if page == "1. Financial Modules":
    st.title("📊 Financial Management")
    # مبيعات ومصروفات (نفس كودك السابق)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales")
        amt = st.number_input("Invoice Amount", min_value=0.0)
        if st.button("Save Sale"): st.session_state.sales_data.append(amt)
    with col2:
        st.subheader("Expenses")
        exp = st.number_input("Expense Cost", min_value=0.0)
        if st.button("Save Expense"): st.session_state.expenses_data.append(exp)
    
    rev = sum(st.session_state.sales_data)
    st.metric("Total Revenue", f"{rev:,.2f} EGP")

elif page == "2. Smart Tax Assistant 🤖":
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

elif page == "3. Team":
    st.table(pd.DataFrame({"Names": ["Omar", "Mennatallah", "Mareez", "Basmala", "Abdelrahman", "Fares", "Mohamed", "Youssef", "Apanob"]}))
