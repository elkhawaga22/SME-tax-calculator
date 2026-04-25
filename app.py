import streamlit as st
import pandas as pd
import requests

# --- 1. Configuration ---
API_KEY = "AIzaSyCULRB3xyOnO9f87qoUVYsSUhqa9yrQRNE"

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
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df, use_container_width=True)
        col1, col2 = st.columns(2)
        col1.metric("Total Revenue", f"EGP {df['Amount'].sum():,.2f}")
        col2.metric("Invoices Count", len(df))

    if st.button("🗑️ Clear All Sales Data"):
        st.session_state.sales_data = []
        st.success("Sales data cleared!")
        st.rerun()

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
            st.rerun()
    
    if st.session_state.expenses_data:
        df_exp = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df_exp, use_container_width=True)
        st.metric("Total Expenses", f"EGP {df_exp['Cost'].sum():,.2f}")

    if st.button("🗑️ Clear All Expenses"):
        st.session_state.expenses_data = []
        st.success("Expenses cleared!")
        st.rerun()

# ==========================
# 3. Tax Dashboard & Report
# ==========================
elif page == "3. Tax Dashboard & Report":
    st.title("📊 Tax Dashboard")
    
    sales_total = sum(i['Amount'] for i in st.session_state.sales_data)
    expenses_total = sum(i['Cost'] for i in st.session_state.expenses_data)
    profit = sales_total - expenses_total
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Revenue", f"EGP {sales_total:,.2f}")
    col2.metric("💸 Expenses", f"EGP {expenses_total:,.2f}")
    col3.metric("💵 Net Profit", f"EGP {profit:,.2f}")
    col4.metric("📈 Profit Margin", f"{(profit/sales_total*100):.1f}%" if sales_total > 0 else "0%")

    tab1, tab2 = st.tabs(["🏢 Law 152 (Simplified)", "📝 Law 91 (General)"])
    
    with tab1:
        st.info("**Law 152/2021 - Simplified Tax System**")
        if sales_total < 1000000:
            tax_152 = 5000
        elif sales_total < 5000000:
            tax_152 = sales_total * 0.01
        else:
            tax_152 = sales_total * 0.015
        st.success(f"**Estimated Tax: EGP {tax_152:,.2f}**")
        st.write("✅ Applies if annual revenue < EGP 10M")
    
    with tab2:
        st.info("**Law 91/2005 - General Tax System**")
        taxable_profit = max(0, profit * 0.8)
        tax_91 = taxable_profit * 0.225
        st.warning(f"**Estimated Tax: EGP {tax_91:,.2f}**")
        st.write("⚠️ Corporate tax rate: 22.5%")

# ==========================
# 4. Smart Tax Assistant (FINAL WORKING VERSION ✅)
# ==========================
elif page == "4. Smart Tax Assistant 🤖":
    st.header("🤖 Smart Tax Assistant")
    st.markdown("**Ask your tax questions in English. I'll analyze your business data!**")
    
    # عرض الرسائل السابقة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if prompt := st.chat_input("Ask about taxes, VAT, deductions..."):
        # User message
        with st.chat_message("user"): 
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("جاري التحليل الضريبي... 🤖"):
                try:
                    # حساب البيانات الحالية
                    sales_total = sum(i['Amount'] for i in st.session_state.sales_data)
                    expenses_total = sum(i['Cost'] for i in st.session_state.expenses_data)
                    profit = sales_total - expenses_total
                    
                    # ✅ الموديلات المتاحة فعلاً في v1beta
                    WORKING_MODELS = [
                        "gemini-1.0-pro-vision-001",
                        "gemini-1.0-pro",
                        "gemini-pro-vision",
                        "gemini-pro"
                    ]
                    
                    # جرب كل موديل لحد ما واحد يشتغل
                    for model_name in WORKING_MODELS:
                        try:
                            API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
                            
                            payload = {
                                "contents": [{
                                    "parts": [{
                                        "text": f"""EGYPTIAN SME TAX EXPERT. Answer SHORT in ENGLISH only.

BUSINESS DATA:
Sales: EGP {sales_total:,.2f} | Expenses: EGP {expenses_total:,.2f} | Profit: EGP {profit:,.2f}

QUESTION: {prompt}

Format:
1. Answer
2. Law (152/91)
3. Action"""
                                    }]
                                }],
                                "generationConfig": {
                                    "temperature": 0.3,
                                    "maxOutputTokens": 300
                                }
                            }
                            
                            response = requests.post(API_URL, json=payload, timeout=20)
                            
                            if response.status_code == 200:
                                data = response.json()
                                if "candidates" in data:
                                    answer = data['candidates'][0]['content']['parts'][0]['text']
                                    st.markdown(answer)
                                    st.session_state.messages.append({"role": "assistant", "content": answer})
                                    break  # نجح! اخرج من اللوب
                                else:
                                    continue
                            else:
                                continue
                                
                        except:
                            continue
                    
                    else:
                        # لو كلهم فشلوا
                        st.error("❌ All models unavailable. Check your API key.")
                        st.info("💡 Test models: gemini-pro, gemini-1.0-pro")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ==========================
# 5. About Page
# ==========================
elif page == "5. About the Project":
    st.title("👥 Project Team")
    st.markdown("**SME Tax Expert - Graduation Project 2026**")
    
    team_data = {
        "Name": ["Omar Mohamed Ahmed", "Mennatallah Moamen", "Mareez Adham", 
                "Basmala Mohamed Saad", "Abdelrahman Ali", "Fares Salah", 
                "Mohamed Hatem", "Youssef Sameh", "Apanob Gamil"],
        "ID": ["2202297", "2200216", "2200243", "2200236", "2200190", 
               "2202312", "2200137", "2200176", "2202995"]
    }
    
    st.dataframe(pd.DataFrame(team_data), use_container_width=True)
    
    st.markdown("""
    ### 📋 Features:
    ✅ Sales & Invoicing | ✅ Expenses Tracking | ✅ Tax Dashboard  
    ✅ AI Tax Assistant | ✅ Law 152/91 Calculator
    
    ### 🎯 Technologies:
    Streamlit • Pandas • Google Gemini API • Egyptian Tax Laws
    """)
    
    st.balloons()
