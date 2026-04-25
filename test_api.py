import streamlit as st
import pandas as pd
import requests

# 🚨 غيّر الـ KEY ده بالـ Key الجديد بتاعك
API_KEY = "AIzaSyDJpTMxu40h_WiDyJZ_WB8TQD2xFmFRnEU"  # <--- هنا

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("SME Tax Expert")
st.sidebar.markdown("Graduation Project 2026") 

page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", "2. Operating Expenses", 
    "3. Tax Dashboard & Report", "4. Smart Tax Assistant 🤖", "5. About"
])

# 1. Sales
if page == "1. Sales & Invoicing":
    st.title("🛒 Sales")
    with st.form("sale"):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client")
        amount = col2.number_input("Amount (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Save"): 
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("✅ Saved!")
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df)
        st.metric("Total Sales", f"EGP {df['Amount'].sum():,.0f}")
    if st.button("🗑️ Clear"): st.session_state.sales_data = []; st.rerun()

# 2. Expenses  
if page == "2. Operating Expenses":
    st.title("💸 Expenses")
    with st.form("exp"):
        col1, col2 = st.columns(2)
        item = col1.text_input("Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Save"): 
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("✅ Saved!")
            st.rerun()
    
    if st.session_state.expenses_data:
        df = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df)
        st.metric("Total Expenses", f"EGP {df['Cost'].sum():,.0f}")
    if st.button("🗑️ Clear"): st.session_state.expenses_data = []; st.rerun()

# 3. Dashboard
if page == "3. Tax Dashboard & Report":
    st.title("📊 Dashboard")
    sales = sum(d['Amount'] for d in st.session_state.sales_data)
    exps = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = sales - exps
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Sales", f"EGP {sales:,.0f}")
    col2.metric("💸 Expenses", f"EGP {exps:,.0f}")
    col3.metric("💵 Profit", f"EGP {profit:,.0f}")
    
    tab1, tab2 = st.tabs(["Law 152", "Law 91"])
    with tab1:
        tax = 5000 if sales < 1_000_000 else sales * 0.01
        st.success(f"Tax: EGP {tax:,.0f}")
    with tab2:
        tax = max(0, profit * 0.225)
        st.warning(f"Tax: EGP {tax:,.0f}")

# 4. AI Assistant (الكود المُختصر والمضمون)
if page == "4. Smart Tax Assistant 🤖":
    st.header("🤖 AI Tax Expert")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if st.button("🗑️ Clear Chat"): st.session_state.messages = []; st.rerun()
    
    prompt = st.chat_input("Ask about Egyptian taxes...")
    if prompt:
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    sales = sum(d['Amount'] for d in st.session_state.sales_data)
                    exps = sum(d['Cost'] for d in st.session_state.expenses_data)
                    
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
                    payload = {
                        "contents": [{"parts": [{"text": f"""Egyptian SME Tax Expert.

Data: Sales EGP{sales:,.0f}, Expenses EGP{exps:,.0f}

Q: {prompt}

Answer SHORT in English."""}]}]
                    }
                    
                    resp = requests.post(url, json=payload, timeout=15)
                    data = resp.json()
                    
                    if resp.status_code == 200:
                        answer = data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("❌ API Error. Check your API Key!")
                        st.info("🔗 Get new key: aistudio.google.com/app/apikey")
                        
                except Exception as e:
                    st.error(f"❌ {e}")

# 5. About
if page == "5. About":
    st.title("👥 Team")
    st.markdown("""
    **SME Tax Expert - 2026**
    
    
