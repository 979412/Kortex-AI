import streamlit as st
import requests
import json
import base64
import io
from groq import Groq
from PIL import Image

# ==========================================================
# 1. ENGINES & CONFIG
# ==========================================================
GEMINI_KEY = "AIzaSyD-X3b959YWreNUSgMj9V1QqNIXKN2o9U0"
GROQ_KEY = "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"
groq_client = Groq(api_key=GROQ_KEY)

st.set_page_config(page_title="ZƏKA ULTRA OMNI-X", layout="wide")

# Şəkli analiz üçün hazırlayan funksiya
def process_image(img_file):
    image = Image.open(img_file).convert("RGB")
    image.thumbnail((800, 800)) # Sürət üçün ölçü
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=80)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# ==========================================================
# 2. ULTRA DESIGN (CSS)
# ==========================================================
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    [data-testid="stChatMessage"] { border-radius: 15px !important; border: 1px solid #f0f0f0; margin-bottom: 10px; }
    .stChatInput { position: fixed; bottom: 20px; }
    header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-weight:900;'>ZƏKA ULTRA <span style='color:red;'>OMNI-X</span></h1>", unsafe_allow_html=True)

# ==========================================================
# 3. MEMORY & LOGIC
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg: st.image(msg["image"], width=300)

# ƏMR GİRİŞİ (Şəkil qəbulu ilə birlikdə)
prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et!"
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        
        # Əgər şəkil varsa, onu dərhal yaddaşa və ekrana ver
        active_img = None
        if prompt.files:
            active_img = Image.open(prompt.files[0])
            st.image(active_img, width=300)
            st.session_state.messages[-1]["image"] = active_img

    # ANALİZ PROSESİ
    with st.chat_message("assistant"):
        with st.spinner("ZƏKA ULTRA DÜŞÜNÜR..."):
            try:
                if active_img:
                    b64_data = process_image(prompt.files[0])
                    
                    # 1. STRATEGIYA: BİRBAŞA GOOGLE API HÜCUMU
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": f"Sən ZƏKA ULTRA-san. Analiz et: {user_text}"},
                                {"inline_data": {"mime_type": "image/jpeg", "data": b64_data}}
                            ]
                        }]
                    }
                    res = requests.post(url, json=payload, timeout=20)
                    
                    if res.status_code == 200:
                        ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    else:
                        # 2. STRATEGIYA: GROQ FALLBACK (Ehtiyat mühərrik)
                        chat_comp = groq_client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
                            ]}]
                        )
                        ans = chat_comp.choices[0].message.content
                else:
                    # SADƏ MƏTN SÖHBƏTİ
                    chat_comp = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": user_text}]
                    )
                    ans = chat_comp.choices[0].message.content

                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})

            except Exception as e:
                st.markdown("Memar, sistemdə anlıq dalğalanma oldu, amma mən hazıram. Əmrinizi gözləyirəm!")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
