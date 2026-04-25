import streamlit as st
import pandas as pd
import requests

# --- 1. Configuration ---
# الـ Key بتاعك اللي بعتهولي
API_KEY = "AIzaSyCULRB3xyOnO9f87qoUVYsSUhqa9yrQRNE"
# الرابط ده بيستخدم v1beta عشان يضمن وصول الـ Flash model
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
# --- 2. Page Config ---
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
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
    st.title("🛒 Sales Management Module")
    with st.form("add_sale"):
        c1, c2 = st.columns(2)
        client = c1.text_input("Client Name")
        amt = c2.number_input("Invoice Amount (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Save Invoice") and amt > 0:
            st.session_state.sales_data.append({"Client": client, "Amount": amt})
            st.success("Invoice saved! ✅")
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Revenue", f"EGP {df['Amount'].sum():,.2f}")

# ==========================
# 2. Operating Expenses
# ==========================
elif page == "2. Operating Expenses":
    st.title("💸 Expenses Module")
    with st.form("add_exp"):
        c1, c2 = st.columns(2)
        item = c1.text_input("Expense Item")
        cost = c2.number_input("Cost (EGP)", min_value=0.0)
        if st.form_submit_button("💾 Record Expense") and cost > 0:
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("Recorded! ✅")
    if st.session_state.expenses_data:
        st.table(pd.DataFrame(st.session_state.expenses_data))

# ==========================
# 3. Tax Dashboard & Report
# ==========================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Tax Dashboard")
    sales = sum(i['Amount'] for i in st.session_state.sales_data)
    exps = sum(i['Cost'] for i in st.session_state.expenses_data)
    profit = sales - exps
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"{sales:,.2f}")
    col2.metric("Expenses", f"{exps:,.2f}")
    col3.metric("Net Profit", f"{profit:,.2f}")

    tab1, tab2 = st.tabs(["🏢 Law 152 (Simplified)", "📝 Law 91 (General)"])
    with tab1:
        tax_152 = 5000 if sales < 1000000 else sales * 0.01 # مثال مبسط
        st.success(f"Law 152 Tax: EGP {tax_152:,.2f}")
    with tab2:
        tax_91 = max(0, profit * 0.225)
        st.warning(f"Law 91 Tax: EGP {tax_91:,.2f}")

# ==========================
# 4. Smart Tax Assistant (THE REQUEST FIX)
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    st.write("Ask your tax questions in English.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask here..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                # الـ Request اللي طلبته يا معلم
                payload = {
                    "contents": [{"parts": [{"text": f"You are an Egyptian tax expert. Answer professionally in English: {prompt}"}]}]
                }
                response = requests.post(API_URL, json=payload)
                data = response.json()
                
                # التأكد من وصول الرد صح
                if "candidates" in data:
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error from Google: {data.get('error', {}).get('message', 'Unknown Error')}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# ==========================
# 5. About Page
# ==========================
elif page == "5. About the Project":
    st.title("Project Team")
    team = {
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    }
    st.table(pd.DataFrame(team))
