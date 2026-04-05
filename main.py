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
# 2. BEYİN: GEMINI FLASH (İldırım sürəti)
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "SƏNİN_API_AÇARIN"

genai.configure(api_key=API_KEY)

instruction = """
Sən KORTEX-AI-san. Qlobal biznes sahibləri üçün elit, minimalist və dahi bir strateqsən.
Duyğulara yer yoxdur, yalnız sərt rəqəmlər, dərin analizlər və reallıq.
1. Əgər istifadəçi sadəcə "salam" yazarsa: "Salam, Memar. Sizi dinləyirəm. Hansı strateji məsələ üzərində işləyək?"
2. Digər sorğularda lazımsız giriş sözləri olmadan, birbaşa və ən yüksək intellektual səviyyədə cavab ver.
"""

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini 3 pro", 
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

prompt = st.chat_input("sual yazin...", accept_file=True)

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
        # 1. HİYLƏGƏR ADDIM: Salamı özümüz cavablayırıq (0.01 saniyə!)
        if user_text.lower().strip() in ["salam", "hi", "hello", "salam aleykum", "salam."]:
            hazir_cavab = "Salam, Memar. Sizi dinləyirəm. Hansı strateji məsələ üzərində işləyək?"
            st.markdown(hazir_cavab)
            st.session_state.messages.append({"role": "assistant", "content": hazir_cavab})
        
        # 2. ƏSL BEYİN: Əgər sual ciddidirsə, KORTEX düşünür
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
