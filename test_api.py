import requests
import json

API_KEY = "AIzaSyCULRB3xyOnO9f87qoUVYsSUhqa9yrQRNE"

# اختبار الموديلات المتاحة
models_to_test = [
    "gemini-pro",
    "gemini-1.0-pro",
    "gemini-pro-vision",
    "gemini-1.0-pro-vision-001"
]

print("🔍 Testing your API Key and available models...\n")

for model in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": "Say hello"}]}],
        "generationConfig": {"temperature": 0.1}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"✅ {model}: OK ({response.status_code})")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result['candidates'][0]['content']['parts'][0]['text'][:50]}...")
        print()
    except Exception as e:
        print(f"❌ {model}: FAILED - {str(e)[:100]}")
        print()

print("🎯 Copy the WORKING model name to your main app!")
