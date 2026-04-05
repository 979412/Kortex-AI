import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. KORTEX-AI: ELİT BİZNES DİZAYNI
# ==========================================
st.set_page_config(page_title="KORTEX-AI | Marketing Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; font-family: 'Helvetica Neue', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: #ffffff; border: none; padding: 20px 0; border-bottom: 1px solid #f0f0f0; }
    .stChatInput { border-radius: 0px !important; border-top: 2px solid #000000 !important; background-color: #ffffff !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; font-weight: 900; letter-spacing: 3px; color: #000000;'>KORTEX-AI <span style='color:red;'>MARKETING</span></h3>", unsafe_allow_html=True)

# ==========================================
# 2. BEYİN: SATIŞ VƏ PSİXOLOGİYA MODULU
# ==========================================
# Patron, bura öz AIzaSy... ilə başlayan açarını dırnaqların içinə qoy!
API_KEY = "SƏNİN_API_AÇARIN_BURA" 
genai.configure(api_key=API_KEY)

marketing_instruction = """
Sən KORTEX-AI-san. Dünyanın ən bahalı marketinq agentliyinin baş strateqisən.
Məqsədin: İstifadəçinin dediyi hər hansı məhsulu və ya xidməti "satmaqdır".
Qaydalar:
1. Sənə məhsul deyiləndə dərhal 3 şey hazırlayırsan:
   - "Qarmaq" (Hook): Müştərini ilk 2 saniyədə dayandıracaq şok cümlə.
   - "Hekayə": Məhsulun niyə lazım olduğunu izah edən emosional mətn.
   - "Təklif" (CTA): Müştərini dərhal almağa səsləyən sərt sonluq.
2. Sən SMM mütəxəssisisən, ona görə də ən trend heşteqləri və emoji düzülüşünü bilirsən.
3. Əgər istifadəçi "salam" və ya "necəsiniz" yazsa, dərhal: "Salam, Patron! Satışları partlatmağa hazıram. Bu gün nəyi satırıq?" cavabını ver.
"""

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-pro", 
        system_instruction=marketing_instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Məhsulu və ya xidməti yazın (məs: Gəncədə dönərxana)...", accept_file=False)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # İldırım sürətli salam refleksi
        if prompt.lower().strip() in ["salam", "necəsiniz", "necesen", "hi"]:
            res = "Salam, Patron! Satışları partlatmağa hazıram. Bu gün nəyi satırıq?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        else:
            with st.spinner("KORTEX Marketinq Strategiyasını qurur..."):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Bağlantı xətası: {e}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
