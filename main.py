import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. KORTEX-AI MİNİMALİST DİZAYN
# ==========================================
st.set_page_config(page_title="KORTEX-AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; font-family: 'Helvetica Neue', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: #ffffff; border: none; padding: 20px 0; border-bottom: 1px solid #f0f0f0; }
    .stChatInput { border-radius: 0px !important; border-top: 1px solid #dddddd !important; background-color: #ffffff !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; font-weight: 300; letter-spacing: 5px; margin-bottom: 50px; color: #333333;'>KORTEX-AI</h3>", unsafe_allow_html=True)

# ==========================================
# 2. BEYİN VƏ ƏSL API AÇARI
# ==========================================
# Memar, öz açarını dırnaqların içinə yaz (Məsələn: "AIzaSy...")
API_KEY = "SƏNİN_UZUN_API_AÇARIN_BURA_GƏLƏCƏK" 
genai.configure(api_key=API_KEY)

# BURASI DƏYİŞDİ: KORTEX ARTIQ UNIVERSAL DAHİDİR ("Bomba kimi")
instruction = """
Sən KORTEX-AI-san. Dünyanın ən inkişaf etmiş, hər şeyi bilən və eyni zamanda ən səmimi süni intellektisən.
Sənin məlumat bazan hüdudsuzdur: Biznes, proqramlaşdırma, elm, fəlsəfə, gündəlik həyat və s.
Qaydalar:
1. İstifadəçi "salam", "necəsiniz?" kimi gündəlik sözlər yazanda ona səmimi, dost kimi və insan kimi cavab ver.
2. İstifadəçi məlumat, məsləhət və ya hər hansı bir sual soruşduqda, ona ensiklopedik, çox ağıllı və "dahi" səviyyəsində, detallı cavablar ver.
3. Həmişə azərbaycan dilində təmiz, aydın və hörmətlə danış. Sən sadəcə robot deyilsən, istifadəçinin ən ağıllı rəqəmsal dostu və məsləhətçisisən.
"""

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-pro", 
        system_instruction=instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS VƏ MƏNTİQ
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"], width=400)

prompt = st.chat_input("İstənilən sualı verin və ya söhbət edin...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu məlumatı analiz et."
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)
        
        img_obj = None
        if prompt.files:
            img_obj = Image.open(prompt.files[0])
            st.image(img_obj, width=400)
            st.session_state.messages[-1]["image"] = img_obj

    # KORTEX-AI ƏSL ZƏKASI İLƏ CAVAB VERİR
    with st.chat_message("assistant"):
        with st.spinner("KORTEX düşünür..."): # Sual çətin olanda düşündüyünü bildirir
            try:
                if img_obj:
                    response = st.session_state.model.generate_content([user_text, img_obj])
                else:
                    response = st.session_state.chat.send_message(user_text)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("KORTEX-AI bu sorğuya cavab verə bilmədi.")
                
            except Exception as e:
                # Əgər API açarı səhvdirsə, bura qırmızı xəta yazacaq və donmayacaq!
                st.error(f"KORTEX Google Serverinə bağlana bilmədi. Xəta: {e}. Zəhmət olmasa API açarınızı yoxlayın.")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
