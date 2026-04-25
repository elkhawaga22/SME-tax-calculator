import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. الإعداد الأساسي بمفتاحك الجديد
API_KEY = "AIzaSyACmy1UgjAVZBpf1sxPAvm0vap8cF_n08Q"

def setup_model():
    try:
        genai.configure(api_key=API_KEY)
        # هذه الخطوة تجلب كل الموديلات المتاحة لمفتاحك فعلياً
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not models:
            return None
            
        # نختار الموديل المتاح (سواء كان pro أو flash)
        # سيبحث عن gemini-1.5-flash أولاً، إذا لم يجده سيأخذ أول موديل متاح
        selected = next((m for m in models if "1.5-flash" in m), models[0])
        return genai.GenerativeModel(selected)
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return None

model = setup_model()

# 2. إعدادات الصفحة
st.set_page_config(page_title="SME Tax Expert 2026", layout="wide")

if 'messages' not in st.session_state: st.session_state.messages = []

# --- الواجهة ---
st.title("🇪🇬 Smart Tax Assistant")
st.sidebar.title("SME Tax Expert")
menu = st.sidebar.radio("Go to", ["Assistant 🤖", "Team 👥"])

if menu == "Assistant 🤖":
    # عرض الشات
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ask me about Egyptian Tax..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            if model:
                try:
                    # نستخدم الموديل الذي تم اختياره تلقائياً
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"AI Error: {e}")
            else:
                st.error("No model found. Check your API Key permissions.")

elif menu == "Team 👥":
    st.write("Project Team: Omar, Mennatallah, Mareez, Basmala, Abdelrahman, Fares, Mohamed, Youssef, Apanob.")
