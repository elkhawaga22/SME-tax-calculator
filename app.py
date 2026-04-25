import streamlit as st
import pandas as pd
import requests

# 1. Configuration
API_KEY = "AIzaSyDJpTMxu40h_WiDyJZ_WB8TQD2xFmFRnEU"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={API_KEY}"

# 2. Page Configuration
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

st.sidebar.title("SME Tax Expert")
st.sidebar.markdown("Graduation Project 2026") 

page = st.sidebar.radio("Navigation", [
    "1. Sales & Invoicing", 
    "2. Operating Expenses", 
    "3. Tax Dashboard & Report",
    "4. Smart Tax Assistant 🤖",
    "5. About the Project"
])

if page == "1. Sales & Invoicing":
    st.title("🛒 Sales Management")
    with st.form("add_sale"):
        col1, col2 = st.columns(2)
        client_name = col1.text_input("Client Name")
        amount = col2.number_input("Amount (EGP)", min_value=0.0)
        if st.form_submit_button("Save") and amount > 0:
            st.session_state.sales_data.append({"Client": client_name, "Amount": amount})
            st.success("Saved!")
    st.dataframe(pd.DataFrame(st.session_state.sales_data))

elif page == "2. Operating Expenses":
    st.title("💸 Expenses")
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        desc = col1.text_input("Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("Record") and cost > 0:
            st.session_state.expenses_data.append({"Item": desc, "Cost": cost})
            st.success("Recorded!")
    st.dataframe(pd.DataFrame(st.session_state.expenses_data))

elif page == "3. Tax Dashboard & Report":
    st.title("📊 Tax Report")
    total_sales = sum(item['Amount'] for item in st.session_state.sales_data)
    total_expenses = sum(item['Cost'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses
    st.metric("Profit", f"{net_profit:,.2f}")
    
    t1, t2 = st.tabs(["Law 152", "Law 91"])
    with t1: st.write(f"Tax: {5000 if total_sales < 1000000 else total_sales * 0.01}")
    with t2: st.write(f"Tax: {max(0, net_profit * 0.225)}")

elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about Egyptian taxes..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                response = requests.post(API_URL, json=payload)
                result = response.json()
                if "candidates" in result:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {result.get('error', {}).get('message', 'Check API Key/Model')}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

elif page == "5. About the Project":
    st.title("Team Members")
    team = {"Name": ["Omar Mohamed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"]}
    st.table(pd.DataFrame(team))
