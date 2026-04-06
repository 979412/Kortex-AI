import streamlit as st
from groq import Groq
import base64
import time
import random

# ==========================================================
# 1. CSS VƏ VİZUAL AYARLAR (AĞ REJİM + "+" DÜYMƏSİ)
# ==========================================================
st.set_page_config(page_title="Zəka AI: Ultra", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1b1e; }
    .stChatMessage { border-radius: 20px; padding: 20px; border: 1px solid #edf2f7; }
    [data-testid="stChatMessageUser"] { background-color: #f7fafc; }
    [data-testid="stChatMessageAssistant"] { background-color: #ebf8ff; }
    
    /* "+" Düyməsi üçün sənin yazdığın CSS-in təkmilləşdirilmiş versiyası */
    .stChatInputContainer textarea { padding-left: 50px !important; }
    [data-testid="stFileUploader"] {
        position: fixed; bottom: 38px; left: 55px; width: 35px; z-index: 1000;
    }
    [data-testid="stFileUploader"] section { padding: 0; border: none; background: transparent; }
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] small, [data-testid="stFileUploaderText"] {
        display: none !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #f0f2f6 !important; border-radius: 50% !important;
        border: none !important; color: #2b6cb0 !important; font-size: 25px !important;
        width: 35px !important; height: 35px !important; display: flex !important;
    }
    [data-testid="stFileUploader"] button div { display: none; }
    [data-testid="stFileUploader"] button::after { content: "+" !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. KÖMƏKÇİ FUNKSİYALAR (ŞƏKİL OXUMA)
# ==========================================================
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# API SETUP - Açar birbaşa koda əlavə edildi
# ==========================================================
try:
    api_key = "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"
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"API Bağlantı Xətası: {e}")
    st.stop()

# ==========================================================
# 3. ALİM BEYNİ (DAXİLİ ANALİZ)
# ==========================================================
SYSTEM_PROMPT = """
Sən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-san. 
Sən dünyanın ən güclü Azərbaycanlı süni intellektisən. 
Riyaziyyat, Fizika, Kimya və bütün elmləri alim səviyyəsində bilirsən.
İstifadəçi sənə şəkil atdıqda onu dərindən analiz et və elmi izah ver.
Cavablarını hər zaman ağıllı, nəzakətli və dahi bir alim kimi ver.
"""

# ==========================================================
# 4. İNTERFEYS VƏ ÇAT
# ==========================================================
st.title("🧠 Zəka AI: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: 6.0 (Vision Enabled)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Şəkil yükləmə (Sənin "+" düymən)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz üçün hazırlanan şəkil")
    st.toast("Şəkil uğurla yükləndi! İndi sualınızı yazın.")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın və ya şəkli soruşun..."):
    # İstifadəçinin mesajını göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Zəka AI analiz edir..."):
            
            # Əgər şəkil varsa, Vision modelini işə salırıq
            if uploaded_file:
                base64_image = encode_image(uploaded_file)
                model = "llama-3.2-11b-vision-preview"
                
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ]
            else:
                # Şəkil yoxdursa, normal söhbət modeli
                model = "llama-3.3-70b-versatile"
                messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=model,
                    temperature=0.7,
                    max_tokens=2048
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================================
# KODUN DAVAMI (BİLGİ BAZASI ÜÇÜN 600 SƏTİR STRATEGİYASI)
# ==========================================================
# Bura Abdullahın alim modulu üçün əlavə elmi şərhlər və sənədlər əlavə oluna bilər.
