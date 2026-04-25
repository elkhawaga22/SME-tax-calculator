import streamlit as st
import pandas as pd
import requests
import json

# 1. Configuration
# استخدم المفتاح الذي نجح معك في التيست
API_KEY = "AIzaSyD7FvVcME2hyYWrLT31u3Ufdeoc3LjjYfQ"

def get_ai_response(prompt):
    # استخدام الإصدار الأكثر استقراراً v1
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.8,
            "topK": 10
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        # التأكد من وجود إجابة قبل محاولة قراءتها
        if "candidates" in result and len(result["candidates"]) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        elif "error" in result:
            return f"AI Error: {result['error']['message']}"
        else:
            return "The AI is busy right now, please try again in a moment."
    except Exception as e:
        return f"Connection Error: {str(e)}"

# 2. Page Configuration
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# Session State
if 'sales' not in st.session_state: st.session_state.sales = []
if 'expenses' not in st.session_state: st.session_state.expenses = []
if 'messages' not in st.session_state: st.session_state.messages = []

# --- Sidebar ---
st.sidebar.title("🏢 SME Tax Expert")
page = st.sidebar.radio("Navigation", ["1. Financials", "2. Smart Assistant 🤖", "3. Team"])

if page == "1. Financials":
    st.title("📊 Tax Management")
    c1, c2 = st.columns(2)
    with c1:
        amt = st.number_input("Add Sale (EGP)", min_value=0.0)
        if st.button("Save Sale"): st.session_state.sales.append(amt)
    with c2:
        exp = st.number_input("Add Expense (EGP)", min_value=0.0)
        if st.button("Save Expense"): st.session_state.expenses.append(exp)
    
    total_rev = sum(st.session_state.sales)
    st.metric("Total Revenue", f"{total_rev:,.2f}")

elif page == "2. Smart Assistant 🤖":
    st.header("Tax Assistant 🤖")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ask here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = get_ai_response(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

elif page == "3. Team":
    st.title("Project Team")
    team = ["Omar", "Mennatallah", "Mareez", "Basmala", "Abdelrahman", "Fares", "Mohamed", "Youssef", "Apanob"]
    st.write(team)
