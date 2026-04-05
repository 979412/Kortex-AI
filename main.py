import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. ULTRA MİNİMALİST DİZAYN (TAM AĞ)
# ==========================================
st.set_page_config(page_title="ZƏKA ULTRA", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; font-family: 'Helvetica Neue', sans-serif; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stChatMessage"] { background-color: #ffffff; border: none; padding: 20px 0; border-bottom: 1px solid #f0f0f0; }
    .stChatInput { border-radius: 0px !important; border-top: 1px solid #dddddd !important; background-color: #ffffff !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; font-weight: 300; letter-spacing: 5px; margin-bottom: 50px; color: #333333;'>ZƏKA ULTRA</h3>", unsafe_allow_html=True)

# ==========================================
# 2. BEYİN: GEMINI PRO (Ən güclü versiya)
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "SƏNİN_API_AÇARIN"

genai.configure(api_key=API_KEY)

instruction = """
Sən ZƏKA ULTRA-san. Qlobal biznes sahibləri üçün elit, minimalist və dahi bir strateqsən.
Duyğulara yer yoxdur, yalnız sərt rəqəmlər, dərin analizlər və reallıq.
1. Əgər istifadəçi "salam" yazarsa: "Salam, Memar. Sizi dinləyirəm. Hansı strateji məsələ üzərində işləyək?"
2. Digər sorğularda birbaşa, ən yüksək intellektual səviyyədə cavab ver.
"""

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest", 
        system_instruction=instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS VƏ CANLI AXIN (STREAMING)
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"], width=400)

prompt = st.chat_input("Əmr et, Memar...", accept_file=True)

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

    # 0.6 SANİYƏ REAKSİYA ÜÇÜN CANLI YAZMA SİSTEMİ
    with st.chat_message("assistant"):
        try:
            # Gözləmə animasiyasını ləğv etdik ki, vaxt itirməyək
            if img_obj:
                response = st.session_state.model.generate_content([user_text, img_obj], stream=True)
            else:
                response = st.session_state.chat.send_message(user_text, stream=True)
            
            # Sözləri gəldiyi anda ekrana "tüpürür"
            def stream_generator():
                for chunk in response:
                    yield chunk.text
                    
            full_response = st.write_stream(stream_generator())
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Gözlənilməz dalğalanma.")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
