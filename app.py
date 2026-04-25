import streamlit as st
import pandas as pd
import requests

# 1. Configuration
# تم وضع المفتاح الخاص بك والربط المباشر بـ v1 لتجنب الـ 404
API_KEY = "AIzaSyDJpTMxu40h_WiDyJZ_WB8TQD2xFmFRnEU"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-exp:generateContent?key={API_KEY}"

# 2. Page Configuration & Styling
st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# --- Database Simulation (Session State) ---
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- Sidebar Menu ---
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
        col1, col2 = st.columns(2)
        client_name = col1.text_input("Client Name")
        amount = col2.number_input("Invoice Amount (EGP)", min_value=0.0, step=100.0)
        if st.form_submit_button("💾 Save Invoice") and amount > 0:
            st.session_state.sales_data.append({"Client": client_name, "Amount": amount})
            st.success("Invoice saved successfully! ✅")
    if st.session_state.sales_data:
        df_sales = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df_sales, use_container_width=True)
        st.metric("Total Revenue", f"EGP {df_sales['Amount'].sum():,.2f}")

# ==========================
# 2. Operating Expenses Module
# ==========================
elif page == "2. Operating Expenses":
    st.title("💸 Expense Management Module")
    with st.form("add_expense"):
        col1, col2 = st.columns(2)
        desc = col1.text_input("Expense Item")
        cost = col2.number_input("Cost (EGP)", min_value=0.0, step=100.0)
        if st.form_submit_button("💾 Record Expense") and cost > 0:
            st.session_state.expenses_data.append({"Item": desc, "Cost": cost})
            st.success("Expense recorded successfully! ✅")
    if st.session_state.expenses_data:
        df_exp = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_exp, use_container_width=True)

# ==========================
# 3. Tax & Dashboard Module
# ==========================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Financial & Tax Report")
    total_sales = sum(item['Amount'] for item in st.session_state.sales_data)
    total_expenses = sum(item['Cost'] for item in st.session_state.expenses_data)
    net_profit = total_sales - total_expenses
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Revenue", f"{total_sales:,.2f}")
    c2.metric("Expenses", f"{total_expenses:,.2f}")
    c3.metric("Profit", f"{net_profit:,.2f}")

    tab1, tab2 = st.tabs(["🏢 Law 152", "📝 Law 91"])
    with tab1:
        tax_152 = 5000 if total_sales < 1000000 else total_sales * 0.01
        st.success(f"Estimated Tax: EGP {tax_152:,.2f}")
    with tab2:
        tax_91 = max(0, net_profit * 0.225)
        st.warning(f"Estimated Tax: EGP {tax_91:,.2f}")

# ==========================
# 4. Smart Tax Assistant (NO MORE 404 ERROR)
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("Smart Tax Assistant 🤖")
    st.write("Welcome! Ask me anything about Egyptian taxes in English.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask here..."):
        with st.chat_message("user"): st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                # إرسال الطلب مباشرة بدون استخدام مكتبة genai المسببة للمشاكل
                payload = {
                    "contents": [{"parts": [{"text": f"You are an Egyptian tax expert for SMEs. Answer professionally in English: {prompt}"}]}]
                }
                response = requests.post(API_URL, json=payload)
                response_data = response.json()
                
                # استخراج النص من رد جوجل
                if "candidates" in response_data:
                    answer = response_data['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"AI Error: {response_data.get('error', {}).get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# ==========================
# 5. About Page
# ==========================
elif page == "5. About the Project":
    st.title("About the Project")
    team_data = {
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", "2202312", "2200137", "2200176", "2202995"]
    }
    st.table(pd.DataFrame(team_data))
