import streamlit as st
import pandas as pd
import requests

# 🚨 حط الـ API Key الجديد هنا
API_KEY = "AIzaSyDJpTMxu40h_WiDyJZ_WB8TQD2xFmFRnEU"  # <--- الـ Key الجديد

st.set_page_config(page_title="SME Tax Expert", layout="wide", page_icon="🇪🇬")

# Session state
if 'sales_data' not in st.session_state: st.session_state.sales_data = []
if 'expenses_data' not in st.session_state: st.session_state.expenses_data = []
if "messages" not in st.session_state: st.session_state.messages = []

# Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
st.sidebar.title("🇪🇬 SME Tax Expert")
page = st.sidebar.radio("القوائم", ["1️⃣ المبيعات", "2️⃣ المصروفات", "3️⃣ لوحة الضرائب", "4️⃣ مساعد ذكي 🤖", "5️⃣ عن المشروع"])

# 1. Sales
if page == "1️⃣ المبيعات":
    st.title("🛒 إدارة المبيعات")
    with st.form("sale_form"):
        col1, col2 = st.columns(2)
        client = col1.text_input("اسم العميل")
        amount = col2.number_input("قيمة الفاتورة (جنيه)", min_value=0.0)
        if st.form_submit_button("💾 حفظ"):
            st.session_state.sales_data.append({"Client": client, "Amount": amount})
            st.success("✅ تم الحفظ!")
            st.rerun()
    
    if st.session_state.sales_data:
        df = pd.DataFrame(st.session_state.sales_data)
        st.dataframe(df, use_container_width=True)
        col1, col2 = st.columns([3,1])
        col1.metric("إجمالي المبيعات", f"{df['Amount'].sum():,.0f} جنيه")
        col2.metric("عدد الفواتير", len(df))
    
    if st.button("🗑️ مسح الكل"): 
        st.session_state.sales_data = []
        st.rerun()

# 2. Expenses
elif page == "2️⃣ المصروفات":
    st.title("💸 إدارة المصروفات")
    with st.form("exp_form"):
        col1, col2 = st.columns(2)
        item = col1.text_input("اسم المصروف")
        cost = col2.number_input("التكلفة (جنيه)", min_value=0.0)
        if st.form_submit_button("💾 حفظ"):
            st.session_state.expenses_data.append({"Item": item, "Cost": cost})
            st.success("✅ تم الحفظ!")
            st.rerun()
    
    if st.session_state.expenses_data:
        df = pd.DataFrame(st.session_state.expenses_data)
        st.dataframe(df, use_container_width=True)
        st.metric("إجمالي المصروفات", f"{df['Cost'].sum():,.0f} جنيه")
    
    if st.button("🗑️ مسح الكل"): 
        st.session_state.expenses_data = []
        st.rerun()

# 3. Dashboard
elif page == "3️⃣ لوحة الضرائب":
    st.title("📊 لوحة الضرائب")
    
    sales_total = sum(d['Amount'] for d in st.session_state.sales_data)
    exp_total = sum(d['Cost'] for d in st.session_state.expenses_data)
    profit = sales_total - exp_total
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 المبيعات", f"{sales_total:,.0f} جنيه")
    col2.metric("💸 المصروفات", f"{exp_total:,.0f} جنيه")
    col3.metric("💵 الربح", f"{profit:,.0f} جنيه")
    
    tab1, tab2 = st.tabs(["قانون 152 (مبسط)", "قانون 91 (عام)"])
    with tab1:
        tax152 = 5000 if sales_total < 1000000 else sales_total * 0.01
        st.success(f"💰 الضريبة المتوقعة: **{tax152:,.0f} جنيه**")
    with tab2:
        tax91 = max(0, profit * 0.225)
        st.warning(f"💰 الضريبة المتوقعة: **{tax91:,.0f} جنيه**")

# 4. AI Assistant - الحل النهائي المضمون
elif page == "4️⃣ مساعد ذكي 🤖":
    st.header("🤖 مساعد الضرائب الذكي")
    st.caption("اسأل بالإنجليزية: What tax law should I use?")
    
    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Chat input
    prompt = st.chat_input("اكتب سؤالك هنا...")
    if prompt:
        # User message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # AI Response
        with st.chat_message("assistant"):
            with st.spinner("🤖 جاري التفكير..."):
                try:
                    # ✅ API v1 (الأحدث والمضمون)
                    sales = sum(d['Amount'] for d in st.session_state.sales_data)
                    expenses = sum(d['Cost'] for d in st.session_state.expenses_data)
                    
                    # جرب v1 أولاً (الأحدث)
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
                    
                    payload = {
                        "contents": [{
                            "parts": [{
                                "text": f"""Egyptian Tax Expert for SMEs.

Business: Sales EGP{sales:,.0f} | Expenses EGP{expenses:,.0f}

Question: {prompt}

Answer in English. Short & professional."""
                            }]
                        }]
                    }
                    
                    response = requests.post(url, json=payload, timeout=20)
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        # Fallback v1beta gemini-pro
                        url2 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
                        response2 = requests.post(url2, json=payload, timeout=10)
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            answer2 = data2['candidates'][0]['content']['parts'][0]['text']
                            st.markdown(answer2)
                            st.session_state.messages.append({"role": "assistant", "content": answer2})
                        else:
                            st.error("❌ API مش شغال")
                            st.info("""
                            🔧 الحل:
                            1. تأكد من الـ API Key
                            2. https://aistudio.google.com/app/apikey
                            3. استخدم الـ Dashboard بدل الـ AI
                            """)
                            
                except Exception as e:
                    st.error(f"خطأ: {e}")

# 5. About
elif page == "5️⃣ عن المشروع":
    st.title("👥 فريق المشروع")
    st.markdown("""
    
