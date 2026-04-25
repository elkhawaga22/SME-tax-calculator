import streamlit as st
import pandas as pd
import requests

# حط الـ API Key الجديد هنا
API_KEY = "AIzaSyDJpTMxu40h_WiDyJZ_WB8TQD2xFmFRnEU"

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: 
    st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: 
    st.session_state.expenses_data = []
if "messages" not in st.session_state: 
    st.session_state.messages = []

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("SME Tax Expert")
page = st.sidebar.radio("Navigation", ["Sales", "Expenses", "Dashboard", "AI Chat", "About"])

# 1. Sales
if page == "Sales":
    st.title("🛒 Sales")
    with st.form("sales"):
        col1, col2 = st.columns(2)
        client = col1.text_input("Client Name")
        amount = col2.number_input("Amount EGP", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("Saved!")
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df)
        st.metric("Total Sales", f"EGP {df['Amount'].sum():,.0f}")
    if st.button("Clear All"):
        st.session_state.sales_data = []
        st.rerun()

# 2. Expenses
elif page == "Expenses":
    st.title("💸 Expenses")
    with st.form("expenses"):
        col1, col2 = st.columns(2)
        item = col1.text_input("Item")
        cost = col2.number_input("Cost EGP", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("Saved!")
            st.rerun()
    
    if st.session_state.expenses_data:
        df = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df)
        st.metric("Total Expenses", f"EGP {df['Cost'].sum():,.0f}")
    if st.button("Clear All"):
        st.session_state.expenses_data = []
        st.rerun()

# 3. Dashboard
elif page == "Dashboard":
    st.title("📊 Tax Dashboard")
    sales = sum(d['Amount'] for d in st.session_state.sales_data)
    expenses = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = sales - expenses
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Sales", f"EGP {sales:,.0f}")
    col2.metric("Expenses", f"EGP {expenses:,.0f}")
    col3.metric("Profit", f"EGP {profit:,.0f}")
    
    tab1, tab2 = st.tabs(["Law 152", "Law 91"])
    with tab1:
        tax = 5000 if sales < 1000000 else sales * 0.01
        st.success(f"Tax: EGP {tax:,.0f}")
    with tab2:
        tax = max(0, profit * 0.225)
        st.warning(f"Tax: EGP {tax:,.0f}")

# 4. AI Chat
elif page == "AI Chat":
    st.header("🤖 Tax Assistant")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    prompt = st.chat_input("Ask about taxes...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    sales = sum(d['Amount'] for d in st.session_state.sales_data)
                    expenses = sum(d['Cost'] for d in st.session_state.expenses_data)
                    
                    # API v1 - الأحدث والمضمون
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
                    
                    payload = {
                        "contents": [{
                            "parts": [{
                                "text": f"Egyptian SME Tax Expert. Sales: EGP{sales:,.0f}, Expenses: EGP{expenses:,.0f}. Question: {prompt}"
                            }]
                        }]
                    }
                    
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("API Error - Check Key")
                        st.info("Works without AI too!")
                except:
                    st.error("Connection error")

# 5. About
elif page == "About":
    st.title("Team")
    st.markdown("""
    **SME Tax Expert**
    
    - Omar Mohamed Ahmed (2202297)
    - Mennatallah Moamen (2200216) 
    - Mareez Adham (2200243)
    """)
