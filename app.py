import streamlit as st
import pandas as pd
import requests  # ضفنا دي عشان نكلم جوجل مباشرة

# 1. Configuration
API_KEY = "AIzaSyCULRB3xyOnO9f87qoUVYsSUhqa9yrQRNE"
# الرابط ده بيروح للإصدار المستقر v1 مباشرة
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# 2. Page Configuration
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- Sidebar ---
st.sidebar.title("SME Tax Expert")
page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", 
    "2. Operating Expenses", 
    "3. Tax Dashboard & Report",
    "4. Smart Tax Assistant 🤖",
    "5. About the Project"
])

# الأجزاء الخاصة بـ Sales و Expenses و Dashboard خليها زي ما هي عندك 
# أنا هركز لك هنا على الجزء اللي فيه المشكلة (رقم 4)

if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management")
    st.info("Record sales here...") # كودك القديم يفضل هنا

elif page == "2. Operating Expenses":
    st.title("💸 Expenses")
    st.info("Record expenses here...") # كودك القديم يفضل هنا

elif page == "3. Tax Dashboard & Report":
    st.title("📊 Tax Report")
    st.info("View dashboard here...") # كودك القديم يفضل هنا

# ==========================
# 4. Smart Tax Assistant (الحل النهائي)
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    st.write("Ask anything about Egyptian Tax Laws (Response in English).")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                # بنبعت الطلب لجوجل بشكل يدوي ومباشر (أضمن طريقة)
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"You are an Egyptian tax expert for SMEs. Answer professionally in English. Question: {prompt}"
                        }]
                    }]
                }
                response = requests.post(API_URL, json=payload)
                result = response.json()
                
                # استخراج الرد
                answer = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error("AI is temporarily unavailable. Please try again in a moment.")

elif page == "5. About the Project":
    st.title("About the Project")
    st.write("Omar Mohamed Ahmed (2202297) & Team")
