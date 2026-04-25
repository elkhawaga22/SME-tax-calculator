import google.generativeai as genai
import os

# ضع الـ API Key الجديد هنا
API_KEY = "AIzaSyD7FvVcME2hyYWrLT31u3Ufdeoc3LjjYfQ"  # ← غير ده!

# أو استخدم متغيرات البيئة (الأفضل للأمان)
# os.environ["GOOGLE_API_KEY"] = "your_new_key"

genai.configure(api_key=API_KEY)

# اختبار سريع
try:
    model = genai.GenerativeModel('gemini-1.5-flash-exp')
    response = model.generate_content("اختبرني!")
    print("✅ نجح! الرد:", response.text[:100])
except Exception as e:
    print("❌ خطأ:", e)
    
