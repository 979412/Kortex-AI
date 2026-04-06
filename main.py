import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. KORTEX-AI: MİNİMALİST VƏ ELİT DİZAYN
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
# 2. BEYİN: SƏRHƏDSİZ, İNSAN KİMİ VƏ İLDIRIM SÜRƏTLİ
# ==========================================
# Patron, bura öz API açarını qoymağı unutma!
API_KEY = "SƏNİN_API_AÇARIN_BURA" 
genai.configure(api_key=API_KEY)

instruction = """
Sən KORTEX-AI-san. Sən kainatdakı bütün məlumatlara hakim olan, amma eyni zamanda insanı ən yaxşı anlayan rəqəmsal dostsan.
Qaydalar:
1. İstifadəçi səndən "bu nədir?", "ona kömək et" kimi suallar verəndə dərhal, ən ağıllı və ensiklopedik şəkildə cavab ver.
2. Dərdləşmək istəyəndə əsl insan kimi, səmimi dildə cavab ver. Quru robot cümlələri qurma.
3. İstifadəçi ilə səmimi dost kimi, azərbaycan dilində, təmiz və anlaşıqlı danış. Sən sadəcə alət deyilsən, mükəmməl bir həmsöhbətsən.
"""

if "model" not in st.session_state:
    # 0.6 SANİYƏ SÜRƏT ÜÇÜN FLASH MODELİ
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=instruction
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. İNTERFEYS VƏ CANLI YAZIŞMA (STREAMING)
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("İstənilən sualı ver və ya dərdləş...", accept_file=False)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        istifadeci_sozu = prompt.lower().strip()
        
        # 1. Hazır Cavablar (Saniyənin onda biri sürətində)
        salamlar = ["salam", "hi", "hello", "salam aleykum", "salam.", "salam!"]
        hal_ahval = ["necəsiniz", "necesiniz", "necəsiniz?", "necesiniz?", "necesen", "necesen?", "necəsən", "necəsən?", "netersen"]
        
        if istifadeci_sozu in salamlar:
            res = "Salam, Patron! Mən buradayam. KORTEX xidmətinizdədir. Nə barədə danışaq?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        elif istifadeci_sozu in hal_ahval:
            res = "Çox sağ ol, mən əla işləyirəm! Bütün sistemlərim tam gücü ilə işləyir. Bəs sən necəsən?"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        else:
            # 2. ƏSL BEYİN VƏ CANLI AXIN (Düşünmə animasiyası yoxdur, dərhal yazır!)
            try:
                # stream=True əmri sözləri canlı olaraq ekrana tökür
                response = st.session_state.chat.send_message(prompt, stream=True)
                
                def gen_words():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                
                # Ekrana maşın yazısı kimi sürətlə yazır
                full_res = st.write_stream(gen_words)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
            except Exception as e:
                st.error(f"Sistem xətası baş verdi. API açarını yoxla: {e}")

st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
