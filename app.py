import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعداد واجهة الصفحة
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# --- محرك الـ AI ---
# ملاحظة: سنسمح لك بإدخال المفتاح يدوياً للتأكد من عمله
st.sidebar.title("Settings ⚙️")
user_api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if user_api_key:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.info("Please enter your API Key in the sidebar to use the AI Assistant.")

# --- تهيئة البيانات ---
if 'messages' not in st.session_state: st.session_state.messages = []

# --- التنقل ---
page = st.sidebar.radio("Navigation", ["Home & Tax Info", "Smart Tax Assistant 🤖"])

if page == "Home & Tax Info":
    st.title("🇪🇬 SME Tax Expert")
    st.write("Welcome to the Tax Management System for 2026.")

elif page == "Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    
    if not user_api_key:
        st.warning("⚠️ Access Denied: Enter a valid API Key in the sidebar.")
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        if prompt := st.chat_input("Ask about Egyptian taxes..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"AI Error: {e}")
