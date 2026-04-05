import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. KORTEX-AI MİNİMALİST DİZAYN (TAM AĞ)
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
# 2. BEYİN: GEMINI PRO (Dərin Anlayış və Düşüncə)
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "SƏNİN_API_AÇARIN"

genai.configure(api_key=API_KEY)

# BURASI DƏYİŞDİ: Artıq o səni dinləyəcək və anlayacaq!
instruction = """
Sən KORTEX-AI-san. Dünyanın ən ağıllı, ən dərin düşünən və istifadəçini ən yaxşı anlayan biznes strateqisən.
Sən sadəcə quru məlumat verən robot deyilsən. Sən istifadəçinin nə demək istədiyini, problemin kökünü hiss edən bir zəkasan.
Qaydalar:
1. İstifadəçi sənə nəsə danışanda, əvvəlcə onun fikrini təsdiqlə, onu başa düşdüyünü insan kimi, səmimi dildə ifadə et.
2. Səmimi və anlayışlı ol, amma biznes məsləhəti verəndə mütləq peşəkar və dahi bir strateq kimi dəqiq addımlar göstər.
3. Həmişə "Biz bu problemi necə həll edə bilərik" yanaşması ilə, ona dəstək olaraq cavab ver.
"""

if "model" not in st.session_state:
    # "gemini-1.5-pro" səni ən yaxşı anlayan, ən dahi modeldir.
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

prompt = st.chat_input("Sualınızı və ya probleminizi yazın...", accept_file=True)

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

    # KORTEX-AI CAVABI
    with st.chat_message("assistant"):
        # Salamlaşmanı da daha səmimi etdik
        if user_text.lower().strip() in ["salam", "hi", "hello", "salam aleykum", "salam."]:
            hazir_cavab = "Salam! Sizi dinləyirəm, buyurun. Bu gün hansı məsələni birlikdə həll edək?"
            st.markdown(hazir_cavab)
            st.session_state.messages.append({"role": "assistant", "content": hazir_cavab})
        
        # ƏSL BEYİN: Dərindən düşünür və anlayır
        else:
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
                st.error(f"Sistem dalğalanması: {e} (API açarınızı yoxlayın)")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
